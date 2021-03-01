#
# This helper module will contain all functions required for updating the
# priority information of the samples
#
import logging
import logging.config

from typing import Any, List, Final, Iterator, Tuple, Dict
from crawler.types import ModifiedRow, Config, SampleDoc, SamplePriorityDoc, ModifiedRowValue
from crawler.db.mongo import (
    get_mongo_collection,
)
from pymongo.database import Database

from crawler.constants import (
    COLLECTION_PRIORITY_SAMPLES,
    FIELD_PROCESSED,
    FIELD_SAMPLE_ID,
    FIELD_MONGODB_ID,
    FIELD_PLATE_BARCODE,
    DART_STATE_PENDING,
    FIELD_SOURCE,
)

from more_itertools import groupby_transform

from crawler.helpers.logging_helpers import LoggingCollection

from crawler.db.mysql import (
    insert_or_update_samples_in_mlwh,
)

from crawler.db.dart import (
    create_dart_sql_server_conn,
    add_dart_plate_if_doesnt_exist,
    add_dart_well_properties,
)

logger = logging.getLogger(__name__)

logging_collection = LoggingCollection()


def update_priority_samples(db: Database, config: Config, add_to_dart: bool) -> None:
    """
    Update any unprocessed priority samples in MLWH and DART with an up to date
    value for the priority attributes (must_sequence and preferentially_sequence);
    after this, all correctly processed priorities from the collection priority_samples
    will be flagged with processed: True

    Arguments:
        db {Database} -- mongo db instance
        config {Config} -- config for mysql and dart connections
    """

    def extract_mongo_id(sample: SampleDoc) -> ModifiedRowValue:
        return sample[FIELD_MONGODB_ID]

    logger.info("**********************************")
    logger.info("Starting Prioritisation of samples")

    samples = query_any_unprocessed_samples(db)

    # Create all samples in MLWH with samples containing both sample and priority sample info
    mlwh_success = update_priority_samples_into_mlwh(samples, config)

    # Add to the DART database if MLWH update was successful
    if mlwh_success:
        logger.info("MLWH insert successful")
        if add_to_dart:
            logger.info("Adding to DART")
            dart_success = insert_plates_and_wells_into_dart(samples, config)
        if not (add_to_dart) or dart_success:
            logger.info("Updating Mongodb priority samples to processed")
            # use stored identifiers to update priority_samples table to processed true
            sample_ids = list(map(extract_mongo_id, samples))
            update_unprocessed_priority_samples_to_processed(db, sample_ids)


def query_any_unprocessed_samples(db: Database) -> List[SamplePriorityDoc]:
    """
    Returns the list of unprocessed priority samples (from priority_samples mongo collection)
    that have at least one related sample (from samples mongo collection).

    Arguments:
        db {Database} -- mongo db instance
    """
    priority_samples_collection = get_mongo_collection(db, COLLECTION_PRIORITY_SAMPLES)

    IMPORTANT_UNPROCESSED_SAMPLES_MONGO_QUERY: Final[List[object]] = [
        # All unprocessed priority samples
        {
            "$match": {FIELD_PROCESSED: False},
        },
        # Joins priority_samples and samples
        {
            "$lookup": {
                "from": "samples",
                "localField": FIELD_SAMPLE_ID,
                "foreignField": FIELD_MONGODB_ID,
                "as": "related_samples",
            }
        },
        # match is required so "Exception: Cannot unpad coordinate" isn't thrown
        # Only priority samples with a sample associated with them
        {"$match": {"related_samples": {"$ne": []}}},
        # Copy all sample attributes into the root of the object (merge sample+priority_sample)
        {"$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$related_samples", 0]}, "$$ROOT"]}}},
        # Prune the branch for related samples as all that info is now in the root of the object
        {"$project": {"related_samples": 0}},
    ]

    value = priority_samples_collection.aggregate(IMPORTANT_UNPROCESSED_SAMPLES_MONGO_QUERY)
    return list(value)


def update_unprocessed_priority_samples_to_processed(db: Database, mongo_sample_ids: list) -> None:
    """
    Update the given samples processed field in mongo to true
    Arguments:
       mongo_sample_ids {list} -- a list of sample mongodb _ids to update
    """
    priority_samples_collection = get_mongo_collection(db, COLLECTION_PRIORITY_SAMPLES)
    for sample_id in mongo_sample_ids:
        priority_samples_collection.update({FIELD_SAMPLE_ID: sample_id}, {"$set": {FIELD_PROCESSED: True}})
    logger.info("Mongo update of processed for priority samples successful")


def logging_message_object() -> Dict:
    return {
        "success": {
            "msg": "MLWH database inserts completed successfully for priority samples",
        },
        "insert_failure": {
            "error_type": "TYPE 28",
            "msg": "MLWH database inserts failed for priority samples",
            "critical_msg": f"Critical error while processing priority samples'",
        },
        "connection_failure": {
            "error_type": "TYPE 29",
            "msg": "MLWH database inserts failed for priority samples, could not connect",
            "critical_msg": "Error writing to MLWH for priority samples, could not create Database connection",
        },
    }


def update_priority_samples_into_mlwh(samples: List[Any], config: Config) -> bool:
    return insert_or_update_samples_in_mlwh(samples, config, True, logging_collection, logging_message_object())


def insert_plates_and_wells_into_dart(docs_to_insert: List[ModifiedRow], config: Config) -> bool:
    """Insert plates and wells into the DART database.
    Create in DART with docs_to_insert

    Arguments:
        docs_to_insert {List[ModifiedRow]} -- List of any unprocessed samples

    Returns:
        {bool} -- True if the insert was successful; otherwise False
    """

    def extract_plate_barcode(sample: SampleDoc) -> ModifiedRowValue:
        return sample[FIELD_PLATE_BARCODE]

    if (sql_server_connection := create_dart_sql_server_conn(config)) is not None:
        try:
            cursor = sql_server_connection.cursor()

            group_iterator: Iterator[Tuple[Any, Any]] = groupby_transform(docs_to_insert, extract_plate_barcode)

            for plate_barcode, samples in group_iterator:
                try:
                    samples = list(samples)
                    centre_config = centre_config_for_samples(config, samples)
                    plate_state = add_dart_plate_if_doesnt_exist(
                        cursor, plate_barcode, centre_config["biomek_labware_class"]
                    )
                    if plate_state == DART_STATE_PENDING:
                        for sample in samples:
                            add_dart_well_properties(cursor, sample, plate_barcode)
                    cursor.commit()
                except Exception as e:
                    logging_collection.add_error(
                        "TYPE 33",
                        f"DART database inserts failed for plate {plate_barcode} in priority samples inserts",
                    )
                    logger.exception(e)
                    # rollback statements executed since previous commit/rollback
                    cursor.rollback()
                    return False

            logger.debug("DART database inserts completed successfully for priority samples")
            return True
        except Exception as e:
            logging_collection.add_error(
                "TYPE 30",
                "DART database inserts failed for priority samples",
            )
            logger.critical(f"Critical error for priority samples: {e}")
            logger.exception(e)
            return False
        finally:
            sql_server_connection.close()
    else:
        logging_collection.add_error(
            "TYPE 31",
            "DART database inserts failed, could not connect, for priority samples",
        )
        logger.critical("Error writing to DART for priority samples, could not create Database connection")
        return False


def centre_config_for_samples(config, samples):
    centre_name = samples[0][FIELD_SOURCE]

    return list(filter(lambda x: x["name"] == centre_name, config.CENTRES))[0]
