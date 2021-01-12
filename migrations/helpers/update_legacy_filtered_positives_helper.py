from types import ModuleType
from typing import List, Optional, Dict
from pandas import DataFrame  # type: ignore
import pandas as pd
from datetime import datetime
import sqlalchemy  # type: ignore
from crawler.types import Sample
from crawler.filtered_positive_identifier import (
    FILTERED_POSITIVE_VERSION_0,
    FILTERED_POSITIVE_VERSION_1,
    FILTERED_POSITIVE_VERSION_2,
)
from crawler.constants import (
    COLLECTION_SAMPLES,
    FIELD_FILTERED_POSITIVE_VERSION,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_PLATE_BARCODE,
    FILTERED_POSITIVE_FIELDS_SET_DATE,
    FIELD_CREATED_AT,
    FIELD_RESULT,
    POSITIVE_RESULT_VALUE,
    V0_V1_CUTOFF_TIMESTAMP,
    V1_V2_CUTOFF_TIMESTAMP,
)
from crawler.db import (
    create_mongo_client,
    get_mongo_collection,
    get_mongo_db,
)
import logging

logger = logging.getLogger(__name__)


def mongo_samples_by_date(config: ModuleType, start_datetime: datetime, end_datetime: datetime) -> List[Sample]:
    """Gets all samples from Mongo created before Crawler started setting filtered positive fields

    Arguments:
        config {ModuleType} -- application config specifying database details

    Returns:
        List[Sample] -- List of Mongo samples created before filtered positive Crawler changes
    """
    with create_mongo_client(config) as client:
        mongo_db = get_mongo_db(config, client)
        samples_collection = get_mongo_collection(mongo_db, COLLECTION_SAMPLES)
        return list(
            samples_collection.find(
                {
                    FIELD_CREATED_AT: {"$gte": start_datetime, "$lte": end_datetime},
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
        config (ModuleType): application config specifying database details
        root_sample_ids (List[str]): [description]
        plate_barcodes (List[str]): [description]
        start_date (str): lower limit on creation date
        end_date (str): upper limit on creation date
        chunk_size (int, optional): [description]. Defaults to 50000.

    Returns:
        DataFrame: [description]
    """
    try:
        db_connection = None

        logger.debug("Getting cherry-picked samples from MLWH")

        # Create an empty DataFrame to merge into
        concat_frame = pd.DataFrame()

        chunk_root_sample_ids = [
            root_sample_ids[x : (x + chunk_size)] for x in range(0, len(root_sample_ids), chunk_size)  # noqa:E203 E501
        ]

        sql_engine = sqlalchemy.create_engine(
            (
                f"mysql+pymysql://{config.MLWH_DB_RO_USER}:{config.MLWH_DB_RO_PASSWORD}"  # type: ignore # noqa: E501
                f"@{config.MLWH_DB_HOST}:{config.MLWH_DB_PORT}"  # type: ignore
            ),
            pool_recycle=3600,
        )
        db_connection = sql_engine.connect()

        ml_wh_db = config.MLWH_DB_DBNAME  # type: ignore
        events_wh_db = config.EVENTS_WH_DB  # type: ignore

        values_index = 0
        for chunk_root_sample_id in chunk_root_sample_ids:
            logger.debug(f"Querying records between {values_index} and {values_index + chunk_size}")

            sql = (
                f"SELECT mlwh_sample.description as `{FIELD_ROOT_SAMPLE_ID}`, mlwh_stock_resource.labware_human_barcode as `{FIELD_PLATE_BARCODE}`"  # noqa: E501
                f" FROM {ml_wh_db}.sample as mlwh_sample"
                f" JOIN {ml_wh_db}.stock_resource mlwh_stock_resource ON (mlwh_sample.id_sample_tmp = mlwh_stock_resource.id_sample_tmp)"  # noqa: E501
                f" JOIN {events_wh_db}.subjects mlwh_events_subjects ON (mlwh_events_subjects.friendly_name = sanger_sample_id)"  # noqa: E501
                f" JOIN {events_wh_db}.roles mlwh_events_roles ON (mlwh_events_roles.subject_id = mlwh_events_subjects.id)"  # noqa: E501
                f" JOIN {events_wh_db}.events mlwh_events_events ON (mlwh_events_roles.event_id = mlwh_events_events.id)"  # noqa: E501
                f" JOIN {events_wh_db}.event_types mlwh_events_event_types ON (mlwh_events_events.event_type_id = mlwh_events_event_types.id)"  # noqa: E501
                f" WHERE mlwh_sample.description IN %(root_sample_ids)s"
                f" AND mlwh_stock_resource.labware_human_barcode IN %(plate_barcodes)s"
                f" AND mlwh_sample.created >= '{start_date}'"
                f" AND mlwh_sample.created < '{end_date}'"
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

            # drop_duplicates is needed because the same 'root sample id' could
            # pop up in two different batches, and then it would
            # retrieve the same rows for that root sample id twice
            # do reset_index after dropping duplicates to make sure the rows are numbered
            # in a way that makes sense
            concat_frame = concat_frame.append(frame).drop_duplicates().reset_index(drop=True)
            values_index += chunk_size
        return concat_frame
    except Exception as e:
        logger.error("Error while connecting to MySQL")
        logger.exception(e)
        return None
    finally:
        if db_connection:
            db_connection.close()


def v0_version_set(config: ModuleType) -> bool:
    """Find if the v0 version has been set in any of the samples.
       This would indicate that the legacy migration has already been run.

    Args:
        config {ModuleType} -- application config specifying database details

    Returns:
        {bool} -- v0 version set in samples
    """
    with create_mongo_client(config) as client:
        mongo_db = get_mongo_db(config, client)
        samples_collection = get_mongo_collection(mongo_db, COLLECTION_SAMPLES)

        num_v0_samples = samples_collection.count_documents(
            {FIELD_FILTERED_POSITIVE_VERSION: FILTERED_POSITIVE_VERSION_0}
        )

        return num_v0_samples > 0


def split_mongo_samples_by_version(
    samples: List[Sample], cp_samples_df_v0: DataFrame, cp_samples_df_v1: DataFrame
) -> Dict[str, List[Sample]]:
    """Split the Mongo samples dataframe based on the v0 cherrypicked samples. Samples
       which have been v0 cherrypicked need to have the v0 filtered positive rules
       applied. The remaining samples need the v1 rule applied.

    Args:
        samples {List[Sample]} -- List of samples from Mongo
        cp_samples_df_v0 {DataFrame} -- DataFrame of v0 cherrypicked samples
        cp_samples_df_v1: {DataFrame} -- DataFrame of v1 cherrypicked samples

    Returns:
        samples_by_version {Dict[List[Sample]]} -- Samples split by version
    """
    v0_cp_samples = []
    if not cp_samples_df_v0.empty:
        v0_cp_samples = cp_samples_df_v0[[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE]].to_numpy().tolist()  # noqa: E501

    v1_cp_samples = []
    if not cp_samples_df_v1.empty:
        v1_cp_samples = cp_samples_df_v1[[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE]].to_numpy().tolist()  # noqa: E501

    v0_samples = []
    v1_samples = []
    v2_samples = []

    counter = 0
    for sample in samples:
        if [sample[FIELD_ROOT_SAMPLE_ID], sample[FIELD_PLATE_BARCODE]] in v0_cp_samples:
            v0_samples.append(sample)
        elif [sample[FIELD_ROOT_SAMPLE_ID], sample[FIELD_PLATE_BARCODE]] in v1_cp_samples:
            v1_samples.append(sample)
        else:
            v2_samples.append(sample)
        counter += 1

        if counter%10000 == 0:
            logger.debug(f"Split {counter} samples by version")

    samples_by_version = {
        FILTERED_POSITIVE_VERSION_0: v0_samples,
        FILTERED_POSITIVE_VERSION_1: v1_samples,
        FILTERED_POSITIVE_VERSION_2: v2_samples,
     }

    return samples_by_version
