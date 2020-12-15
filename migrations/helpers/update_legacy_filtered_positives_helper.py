from types import ModuleType
from typing import List, Optional, Set, Tuple, Dict
from pandas import DataFrame # type: ignore
import pandas as pd
from datetime import datetime
import sqlalchemy  # type: ignore
from crawler.types import Sample
from crawler.filtered_positive_identifier import (
    FilteredPositiveIdentifier,
    FilteredPositiveIdentifierV0,
    FilteredPositiveIdentifierV1,
    FilteredPositiveIdentifierV2,
    FILTERED_POSITIVE_VERSION_0,
    FILTERED_POSITIVE_VERSION_1,
    FILTERED_POSITIVE_VERSION_2,
)
from migrations.helpers.update_filtered_positives_helper import update_filtered_positive_fields
from crawler.constants import (
    COLLECTION_SAMPLES,
    FIELD_FILTERED_POSITIVE,
    FIELD_FILTERED_POSITIVE_VERSION,
    FIELD_FILTERED_POSITIVE_TIMESTAMP,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_PLATE_BARCODE,
    FIELD_COORDINATE,
)
from crawler.db import (
    create_mongo_client,
    get_mongo_collection,
    get_mongo_db,
)
import logging

logger = logging.getLogger(__name__)


def unmigrated_mongo_samples(config: ModuleType):
    """Gets all samples from Mongo which have not had the filtered positive field set

    Arguments:
        None

    Returns:
        List[Dict] -- All unmigrated samples from Mongo
    """
    with create_mongo_client(config) as client:
        mongo_db = get_mongo_db(config, client)
        samples_collection = get_mongo_collection(mongo_db, COLLECTION_SAMPLES)

        return list(
            samples_collection.find(
                {
                    "$and": [
                        {FIELD_FILTERED_POSITIVE: {"$exists": False}},
                        {FIELD_FILTERED_POSITIVE_VERSION: {"$exists": False}},
                        {FIELD_FILTERED_POSITIVE_TIMESTAMP: {"$exists": False}},
                    ]
                }
            )
        )


def get_cherrypicked_samples_by_date(
    config: ModuleType,
    root_sample_ids: List[str],
    plate_barcodes: List[str],
    start_date: str,
    end_date: str,
    chunk_size: int = 50000,
) -> Optional[DataFrame]:
    """Find which samples have been cherrypicked between defined dates using MLWH & Events warehouse.
    Returns dataframe with 4 columns: those needed to uniquely identify the sample resulting
    dataframe only contains those samples that have been cherrypicked (those that have an entry
    for the relevant event type in the event warehouse)

    Args:
        root_sample_ids (List[str]): [description]
        plate_barcodes (List[str]): [description]
        chunk_size (int, optional): [description]. Defaults to 50000.

    Returns:
        DataFrame: [description]
    """
    try:
        logger.debug("Getting cherry-picked samples from MLWH")

        # Create an empty DataFrame to merge into
        concat_frame = pd.DataFrame()

        chunk_root_sample_ids = [
            root_sample_ids[x : (x + chunk_size)] for x in range(0, len(root_sample_ids), chunk_size)  # noqa:E203
        ]

        sql_engine = sqlalchemy.create_engine(
            (
                f"mysql+pymysql://{config.MLWH_DB_RO_USER}:{config.MLWH_DB_RO_PASSWORD}"  # type: ignore
                f"@{config.MLWH_DB_HOST}"  # type: ignore
            ),
            pool_recycle=3600,
        )
        db_connection = sql_engine.connect()

        ml_wh_db = config.MLWH_DB_DBNAME  # type: ignore
        events_wh_db = config.EVENTS_WH_DB  # type: ignore

        for chunk_root_sample_id in chunk_root_sample_ids:
            sql = (
                f"SELECT mlwh_sample.description as `{FIELD_ROOT_SAMPLE_ID}`, mlwh_stock_resource.labware_human_barcode as `{FIELD_PLATE_BARCODE}`"  # noqa: E501
                f" FROM {ml_wh_db}.sample as mlwh_sample"
                f" JOIN {ml_wh_db}.stock_resource mlwh_stock_resource ON (mlwh_sample.id_sample_tmp = mlwh_stock_resource.id_sample_tmp)"  # noqa: E501
                f" JOIN {events_wh_db}.subjects mlwh_events_subjects ON (mlwh_events_subjects.friendly_name = sanger_sample_id)"  # noqa: E501
                f" JOIN {events_wh_db}.roles mlwh_events_roles ON (mlwh_events_roles.subject_id = mlwh_events_subjects.id)"  # noqa: E501
                f" JOIN {events_wh_db}.events mlwh_events_events ON (mlwh_events_roles.event_id = mlwh_events_events.id)"  # noqa: E501
                f" JOIN {events_wh_db}.event_types mlwh_events_event_types ON (mlwh_events_events.event_type_id = mlwh_events_event_types.id)"  # noqa: E501
                f" WHERE mlwh_sample.description IN %(root_sample_ids)s"
                f" AND mlwh_sample.created BETWEEN '{start_date}' AND '{end_date}'"
                f" AND mlwh_stock_resource.labware_human_barcode IN %(plate_barcodes)s"
                " AND mlwh_events_event_types.key = 'cherrypick_layout_set'"
                " GROUP BY mlwh_sample.description, mlwh_stock_resource.labware_human_barcode, mlwh_sample.phenotype, mlwh_stock_resource.labware_coordinate"  # noqa: E501
            )

            frame = pd.read_sql(
                sql,
                db_connection,
                params={
                    "root_sample_ids": tuple(chunk_root_sample_id),
                    "plate_barcodes": tuple(plate_barcodes),
                },
            )

            # drop_duplicates is needed because the same 'root sample id' could pop up in two different batches,
            # and then it would retrieve the same rows for that root sample id twice
            # do reset_index after dropping duplicates to make sure the rows are numbered in a way that makes sense
            concat_frame = concat_frame.append(frame).drop_duplicates().reset_index(drop=True)

        return concat_frame
    except Exception as e:
        logger.error("Error while connecting to MySQL")
        logger.exception(e)
        return None
    finally:
        db_connection.close()


def check_versions_set(config: ModuleType):
    """Find if the v0 or v1 version has been set in any of the samples. This would indicate that the legacy migration has already been run.

    Args:
        samples {List[Dict]} -- List of samples from Mongo

    Returns:
        Boolean -- v0 version set in samples
    """
    with create_mongo_client(config) as client:
        mongo_db = get_mongo_db(config, client)
        samples_collection = get_mongo_collection(mongo_db, COLLECTION_SAMPLES)

        v0_samples = list(
            samples_collection.find(
                {
                    "$or": [
                        {FIELD_FILTERED_POSITIVE_VERSION: FILTERED_POSITIVE_VERSION_0},
                        {FIELD_FILTERED_POSITIVE_VERSION: FILTERED_POSITIVE_VERSION_1},
                    ]
                }
            )
        )
        if len(v0_samples) > 0:
            return True
        else:
            return False


def split_mongo_samples_by_version(samples: List[Sample], cp_samples_df_v0: DataFrame, cp_samples_df_v1: DataFrame):
    """Split the Mongo samples dataframe based on the v0 cherrypicked samples. Samples
       which have been v0 cherrypicked need to have the v0 filtered positive rules
       applied. The remaining samples need the v1 rule applied.

    Args:
        samples {List[Sample]} -- List of samples from Mongo
        cp_samples_df_v0: DataFrame -- DataFrame of v0 cherrypicked samples
        cp_samples_df_v1: DataFrame -- DataFrame of v1 cherrypicked samples

    Returns:
        samples_by_version {Dict[List[Sample]]} -- Samples split by version
    """
    v0_cp_samples = cp_samples_df_v0[[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE]].to_numpy().tolist()
    v1_cp_samples = cp_samples_df_v1[[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE]].to_numpy().tolist()

    v0_unmigrated_samples = []
    v1_unmigrated_samples = []
    v2_unmigrated_samples = []

    for sample in samples:
        if [sample[FIELD_ROOT_SAMPLE_ID], sample[FIELD_PLATE_BARCODE]] in v0_cp_samples:
            v0_unmigrated_samples.append(sample)
        elif [sample[FIELD_ROOT_SAMPLE_ID], sample[FIELD_PLATE_BARCODE]] in v1_cp_samples:
            v1_unmigrated_samples.append(sample)
        else:
            v2_unmigrated_samples.append(sample)



    samples_by_version = {
        FILTERED_POSITIVE_VERSION_0: v0_unmigrated_samples,
        FILTERED_POSITIVE_VERSION_1: v1_unmigrated_samples,
        FILTERED_POSITIVE_VERSION_2: v2_unmigrated_samples,
    }

    return samples_by_version


def update_filtered_positive_fields_by_version(samples_by_version: Dict[str, List[Sample]]):
    """Loop through filtered positive versions and update sample fields accordingly

    Args:
        samples_by_version {Dict[List[Sample]]} -- Samples split by version rule to be applied

    Returns:
        migrated_samples {List[Sample]} -- Samples with filtered positive rules applied
    """
    filtered_positive_identifiers = {
        FILTERED_POSITIVE_VERSION_0: FilteredPositiveIdentifierV0(),
        FILTERED_POSITIVE_VERSION_1: FilteredPositiveIdentifierV1(),
        FILTERED_POSITIVE_VERSION_2: FilteredPositiveIdentifierV2(),
    }

    migrated_samples = []
    update_timestamp = datetime.now()
    for version, version_samples in samples_by_version.items():
        filtered_positive_identifier = filtered_positive_identifiers[version]

        logger.info(f"Updating {version} filtered positives...")
        update_filtered_positive_fields(
            filtered_positive_identifier,
            version_samples,
            version,
            update_timestamp,
        )
        migrated_samples.extend(version_samples)
    
    return migrated_samples
