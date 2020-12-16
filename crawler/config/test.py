from crawler.config.defaults import *  # noqa: F403,F401
from crawler.constants import FIELD_RNA_ID, LOCALHOST, ROOT_PASSWORD

# settings here overwrite those in defaults.py

# general details
DIR_DOWNLOADED_DATA = "tests/files/"

# centre details
CENTRES = [
    {
        "barcode_field": FIELD_RNA_ID,
        "barcode_regex": r"^(.*)_([A-Z]\d\d)$",
        "name": "Alderley",
        "prefix": "ALDP",
        "lab_id_default": "AP",
        "backups_folder": "tmp/backups/ALDP",
        "sftp_file_regex": r"^AP_sanger_report_(\d{6}_\d{4})\.csv$",
        "sftp_root_read": "tests/files",
        "file_names_to_ignore": [],
        "biomek_labware_class": "KingFisher_96_2ml",
    },
    {
        "barcode_field": FIELD_RNA_ID,
        "barcode_regex": r"^(.*)_([A-Z]\d\d)$",
        "name": "UK Biocentre",
        "prefix": "MILK",
        "lab_id_default": "MK",
        "backups_folder": "tmp/backups/MILK",
        "sftp_file_regex": r"^MK_sanger_report_(\d{6}_\d{4})\.csv$",
        "sftp_root_read": "tests/files",
        "file_names_to_ignore": [],
        "biomek_labware_class": "KingFisher_96_2ml",
    },
    {
        "barcode_field": FIELD_RNA_ID,
        "barcode_regex": r"^(.*)_([A-Z]\d\d)$",
        "name": "Test Centre",
        "prefix": "TEST",
        "lab_id_default": "TE",
        "backups_folder": "tmp/backups/TEST",
        "sftp_file_regex": r"^TEST_sanger_report_(\d{6}_\d{4})\.csv$",
        "sftp_root_read": "tests/files",
        "file_names_to_ignore": ["TEST_sanger_report_200518_2205.csv"],
        "biomek_labware_class": "KingFisher_96_2ml",
    },
    {
        "barcode_field": FIELD_RNA_ID,
        "barcode_regex": r"^(.*)_([A-Z]\d\d)$",
        "name": "Cambridge-az",
        "prefix": "CAMC",
        "lab_id_default": "CB",
        "backups_folder": "tmp/backups/CAMC",
        "sftp_file_regex": r"^CB_sanger_report_(\d{6}_\d{4})\.csv$",
        "sftp_root_read": "project-heron_cambridge-az",
        "file_names_to_ignore": [],
        "biomek_labware_class": "Bio-Rad_96PCR",
    },
]

# SFTP details
SFTP_UPLOAD = False
SFTP_HOST = LOCALHOST
SFTP_PASSWORD = "pass"
SFTP_PORT = "22"
SFTP_USER = "foo"

# MongoDB details
MONGO_HOST = LOCALHOST
MONGO_DB = "crawlerTestDB"

# MLWH database details
MLWH_DB_DBNAME = "unified_warehouse_test"
MLWH_DB_HOST = LOCALHOST
MLWH_DB_PORT = 3306
MLWH_DB_RO_USER = "root"
MLWH_DB_RO_PASSWORD = ROOT_PASSWORD
MLWH_DB_RW_USER = "root"
MLWH_DB_RW_PASSWORD = ROOT_PASSWORD

# DART database details
DART_DB_DBNAME = "dart_test"
# DART_DB_HOST = "127.0.0.1"
DART_DB_HOST = "host.docker.internal"
DART_DB_PORT = 1433
DART_DB_RW_USER = "root"
DART_DB_RW_PASSWORD = ""
DART_DB_DRIVER = "{ODBC Driver 17 for SQL Server}"

# logging config
LOGGING["loggers"]["crawler"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["crawler"]["handlers"] = ["colored_stream"]  # noqa: F405
