from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import dateutil.parser

from crawler.constants import (
    EVENT_CHERRYPICK_LAYOUT_SET,
    FIELD_COORDINATE,
    FIELD_CREATED_AT,
    FIELD_FILTERED_POSITIVE,
    FIELD_FILTERED_POSITIVE_TIMESTAMP,
    FIELD_FILTERED_POSITIVE_VERSION,
    FIELD_MONGODB_ID,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
    FILTERED_POSITIVE_FIELDS_SET_DATE,
    MLWH_COORDINATE,
    MLWH_FILTERED_POSITIVE,
    MLWH_FILTERED_POSITIVE_TIMESTAMP,
    MLWH_FILTERED_POSITIVE_VERSION,
    MLWH_MONGODB_ID,
    MLWH_PLATE_BARCODE,
    MLWH_RESULT,
    MLWH_RNA_ID,
    MLWH_ROOT_SAMPLE_ID,
    PLATE_EVENT_DESTINATION_CREATED,
    POSITIVE_RESULT_VALUE,
    V0_V1_CUTOFF_TIMESTAMP,
    V1_V2_CUTOFF_TIMESTAMP,
    FIELD_MUST_SEQUENCE,
    FIELD_PREFERENTIALLY_SEQUENCE,
    FIELD_PROCESSED,
)

TESTING_SAMPLES: List[Dict[str, Union[str, bool]]] = [
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        "released": True,
        FIELD_RNA_ID: "A01aaa",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
    },
    {
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        "released": False,
        FIELD_RNA_ID: "B01aaa",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
    },
    {
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_RNA_ID: "C01aaa",
    },
    {
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "456",
        "released": True,
        FIELD_ROOT_SAMPLE_ID: "MCM004",
        FIELD_RNA_ID: "D01aaa",
    },
]

TESTING_PRIORITY_SAMPLES: List[Dict[str, Union[str, bool]]] = [
    {
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False
    },
    {
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: True,
        FIELD_PROCESSED: False
    },
    {
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: True
    },
    {
        FIELD_ROOT_SAMPLE_ID: "MCM004",
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False
    }
]

TESTING_PRIORITY_SAMPLES_FOR_ALDP: List[Dict[str, Union[str, bool]]] = [
    {
        FIELD_ROOT_SAMPLE_ID: "1",
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False
    },
    {
        FIELD_ROOT_SAMPLE_ID: "2",
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: True,
        FIELD_PROCESSED: False
    },
    {
        FIELD_ROOT_SAMPLE_ID: "3",
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: True
    },
    {
        FIELD_ROOT_SAMPLE_ID: "4",
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False
    },
    {
        FIELD_ROOT_SAMPLE_ID: "5",
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False
    }
]


FILTERED_POSITIVE_TESTING_SAMPLES: List[Dict[str, Union[str, bool, datetime]]] = [
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        "released": True,
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_FILTERED_POSITIVE: True,
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
        FIELD_FILTERED_POSITIVE_VERSION: "v2",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) + timedelta(days=1),
    },
    {
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        "released": False,
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_FILTERED_POSITIVE: True,
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
        FIELD_FILTERED_POSITIVE_VERSION: "v2",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) + timedelta(days=1),
    },
    {
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_FILTERED_POSITIVE: False,
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
        FIELD_FILTERED_POSITIVE_VERSION: "v2",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) + timedelta(days=1),
    },
    {
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_FILTERED_POSITIVE: False,
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
        FIELD_FILTERED_POSITIVE_VERSION: "v0",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) - timedelta(days=1),
    },
    {
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: POSITIVE_RESULT_VALUE,
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) - timedelta(days=1),
    },
    {
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test2",
        FIELD_RESULT: POSITIVE_RESULT_VALUE,
        FIELD_PLATE_BARCODE: "456",
        FIELD_ROOT_SAMPLE_ID: "MCM004",
        FIELD_CREATED_AT: dateutil.parser.parse(FILTERED_POSITIVE_FIELDS_SET_DATE) - timedelta(days=2),
    },
]

MONGO_SAMPLES_WITHOUT_FILTERED_POSITIVE_FIELDS: List[Dict[str, Union[str, bool]]] = [
    {
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM004",
    },
    {
        FIELD_COORDINATE: "E01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "456",
        FIELD_ROOT_SAMPLE_ID: "MCM005",
    },
    {
        FIELD_COORDINATE: "E01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "456",
        FIELD_ROOT_SAMPLE_ID: "MCM006",
    },
    {
        FIELD_COORDINATE: "F01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "456",
        FIELD_ROOT_SAMPLE_ID: "MCM007",
    },
]

MONGO_SAMPLES_WITH_FILTERED_POSITIVE_FIELDS = [
    {
        FIELD_MONGODB_ID: "1",
        FIELD_COORDINATE: "A01",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_RNA_ID: "AAA123",
        FIELD_FILTERED_POSITIVE: True,
        FIELD_FILTERED_POSITIVE_VERSION: "v2",
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
    },
    {
        FIELD_MONGODB_ID: "2",
        FIELD_COORDINATE: "B01",
        FIELD_PLATE_BARCODE: "123",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_RNA_ID: "BBB123",
        FIELD_FILTERED_POSITIVE: False,
        FIELD_FILTERED_POSITIVE_VERSION: "v2",
        FIELD_FILTERED_POSITIVE_TIMESTAMP: "2020-01-01T00:00:00.000Z",
    },
]

MLWH_SAMPLES_WITH_FILTERED_POSITIVE_FIELDS = [
    {
        MLWH_MONGODB_ID: "1",
        MLWH_COORDINATE: "A1",
        MLWH_PLATE_BARCODE: "123",
        MLWH_ROOT_SAMPLE_ID: "MCM001",
        MLWH_RNA_ID: "AAA123",
        MLWH_RESULT: POSITIVE_RESULT_VALUE,
        MLWH_FILTERED_POSITIVE: None,
        MLWH_FILTERED_POSITIVE_VERSION: None,
        MLWH_FILTERED_POSITIVE_TIMESTAMP: None,
    },
    {
        MLWH_MONGODB_ID: "2",
        MLWH_COORDINATE: "B1",
        MLWH_PLATE_BARCODE: "123",
        MLWH_ROOT_SAMPLE_ID: "MCM002",
        MLWH_RNA_ID: "BBB123",
        MLWH_RESULT: POSITIVE_RESULT_VALUE,
        MLWH_FILTERED_POSITIVE: True,
        MLWH_FILTERED_POSITIVE_VERSION: "v1.0",
        MLWH_FILTERED_POSITIVE_TIMESTAMP: datetime(2020, 4, 23, 14, 40, 8),
    },
]

EVENT_WH_DATA: Dict[str, Any] = {
    "subjects": [
        {"id": 1, "uuid": "1".encode("utf-8"), "friendly_name": "ss1", "subject_type_id": 1},
        {"id": 2, "uuid": "2".encode("utf-8"), "friendly_name": "ss2", "subject_type_id": 1},
        {"id": 3, "uuid": "3".encode("utf-8"), "friendly_name": "ss3", "subject_type_id": 1},
        {"id": 4, "uuid": "6".encode("utf-8"), "friendly_name": "ss1-beck", "subject_type_id": 1},
        {"id": 5, "uuid": "7".encode("utf-8"), "friendly_name": "ss2-beck", "subject_type_id": 1},
    ],
    "roles": [
        {"id": 1, "event_id": 1, "subject_id": 1, "role_type_id": 1},
        {"id": 2, "event_id": 2, "subject_id": 2, "role_type_id": 1},
        {"id": 3, "event_id": 3, "subject_id": 3, "role_type_id": 1},
        {"id": 4, "event_id": 5, "subject_id": 4, "role_type_id": 1},
        {"id": 5, "event_id": 6, "subject_id": 5, "role_type_id": 1},
    ],
    "events": [
        {
            "id": 1,
            "lims_id": "SQSCP",
            "uuid": "1".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2020-09-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 2,
            "lims_id": "SQSCP",
            "uuid": "2".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2020-10-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 3,
            "lims_id": "SQSCP",
            "uuid": "3".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2020-10-15 16:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 4,
            "lims_id": "SQSCP",
            "uuid": "4".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2020-10-15 16:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 5,
            "lims_id": "SQSCP",
            "uuid": "5".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2020-10-15 16:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 6,
            "lims_id": "SQSCP",
            "uuid": "6".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2020-10-15 16:35:30",
            "user_identifier": "test@example.com",
        },
    ],
    "event_types": [
        {"id": 1, "key": EVENT_CHERRYPICK_LAYOUT_SET, "description": "stuff"},
        {"id": 2, "key": PLATE_EVENT_DESTINATION_CREATED, "description": "stuff"},
    ],
    "subject_types": [{"id": 1, "key": "sample", "description": "stuff"}],
    "role_types": [{"id": 1, "key": "sample", "description": "stuff"}],
}

MLWH_SAMPLE_STOCK_RESOURCE: Dict[str, Any] = {
    "sample": [
        {
            "id_sample_tmp": "1",
            "id_sample_lims": "1",
            "description": "root_1",
            "supplier_name": "cog_uk_id_1",
            "phenotype": "positive",
            "sanger_sample_id": "ss1",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": str(
                datetime.strptime(V0_V1_CUTOFF_TIMESTAMP, "%Y-%m-%d %H:%M:%S")
            ),  # Created at v0/v1 cut-off time
            "uuid_sample_lims": "1",
        },
        {
            "id_sample_tmp": "2",
            "id_sample_lims": "2",
            "description": "root_2",
            "supplier_name": "cog_uk_id_2",
            "phenotype": "positive",
            "sanger_sample_id": "ss2",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": str(
                datetime.strptime(V0_V1_CUTOFF_TIMESTAMP, "%Y-%m-%d %H:%M:%S") - timedelta(days=1)
            ),  # Created before v0/v1 cut-off time
            "uuid_sample_lims": "2",
        },
        {
            "id_sample_tmp": "3",
            "id_sample_lims": "3",
            "description": "root_3",
            "supplier_name": "cog_uk_id_3",
            "phenotype": "positive",
            "sanger_sample_id": "ss3",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": str(
                datetime.strptime(V0_V1_CUTOFF_TIMESTAMP, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
            ),  # Created after v0/v1 cut-off time
            "uuid_sample_lims": "3",
        },
        {
            "id_sample_tmp": "4",
            "id_sample_lims": "4",
            "description": "root_4",
            "supplier_name": "cog_uk_id_4",
            "phenotype": "positive",
            "sanger_sample_id": "ss4",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": str(
                datetime.strptime(V1_V2_CUTOFF_TIMESTAMP, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
            ),  # Created after v1/v2 cut-off time
            "uuid_sample_lims": "4",
        },
        {
            "id_sample_tmp": "5",
            "id_sample_lims": "5",
            "description": "root_1",
            "supplier_name": "cog_uk_id_5",
            "phenotype": "positive",
            "sanger_sample_id": "ss5",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": str(
                datetime.strptime(FILTERED_POSITIVE_FIELDS_SET_DATE, "%Y-%m-%d") + timedelta(days=1)
            ),  # Created after filtered positive fields set
            "uuid_sample_lims": "5",
        },
    ],
    "stock_resource": [
        {
            "id_stock_resource_tmp": "1",
            "id_sample_tmp": "1",
            "labware_human_barcode": "pb_1",
            "labware_machine_barcode": "pb_1",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "1",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "2",
            "id_sample_tmp": "2",
            "labware_human_barcode": "pb_2",
            "labware_machine_barcode": "pb_2",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "2",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "3",
            "id_sample_tmp": "3",
            "labware_human_barcode": "pb_3",
            "labware_machine_barcode": "pb_3",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "3",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "4",
            "id_sample_tmp": "4",
            "labware_human_barcode": "pb_3",
            "labware_machine_barcode": "pb_3",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "4",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "5",
            "id_sample_tmp": "5",
            "labware_human_barcode": "pb_3",
            "labware_machine_barcode": "pb_3",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "5",
            "labware_type": "well",
        },
    ],
    "study": [
        {
            "id_study_tmp": "1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "id_study_lims": "1",
            "id_lims": "SQSCP",
        }
    ],
}


MLWH_SAMPLE_LIGHTHOUSE_SAMPLE: Dict[str, Any] = {
    "sample": [
        {
            "id_sample_tmp": "6",
            "id_sample_lims": "6",
            "description": "root_5",
            "supplier_name": "cog_uk_id_6",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss1",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "36000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "7",
            "id_sample_lims": "7",
            "description": "root_6",
            "supplier_name": "cog_uk_id_7",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss2",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "37000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "8",
            "id_sample_lims": "8",
            "description": "root_5",
            "supplier_name": "cog_uk_id_8",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss3",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "38000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "9",
            "id_sample_lims": "9",
            "description": "root_4",
            "supplier_name": "cog_uk_id_9",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss4",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "39000000000000000000000000000000",
        },
    ],
    "lighthouse_sample": [
        {
            "mongodb_id": "1",
            "root_sample_id": "root_5",
            "rna_id": "pb_4_A01",
            "plate_barcode": "pb_4",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "36000000000000000000000000000000",
        },
        {
            "mongodb_id": "2",
            "root_sample_id": "root_6",
            "rna_id": "pb_5_A01",
            "plate_barcode": "pb_5",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "37000000000000000000000000000000",
        },
        {
            "mongodb_id": "3",
            "root_sample_id": "root_5",
            "rna_id": "pb_6_A01",
            "plate_barcode": "pb_6",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "38000000000000000000000000000000",
        },
        {
            "mongodb_id": "4",
            "root_sample_id": "root_4",
            "rna_id": "pb_3_A01",
            "plate_barcode": "pb_3",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "39000000000000000000000000000000",
        },
    ],
}
