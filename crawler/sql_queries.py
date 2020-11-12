# SQL query to insert multiple rows into the MLWH
SQL_MLWH_MULTIPLE_INSERT = """
INSERT INTO lighthouse_sample (
mongodb_id,
root_sample_id,
rna_id,
plate_barcode,
coordinate,
result,
date_tested_string,
date_tested,
source,
lab_id,
ch1_target,
ch1_result,
ch1_cq,
ch2_target,
ch2_result,
ch2_cq,
ch3_target,
ch3_result,
ch3_cq,
ch4_target,
ch4_result,
ch4_cq,
filtered_positive,
filtered_positive_version,
filtered_positive_timestamp,
created_at,
updated_at
)
VALUES (
%(mongodb_id)s,
%(root_sample_id)s,
%(rna_id)s,
%(plate_barcode)s,
%(coordinate)s,
%(result)s,
%(date_tested_string)s,
%(date_tested)s,
%(source)s,
%(lab_id)s,
%(ch1_target)s,
%(ch1_result)s,
%(ch1_cq)s,
%(ch2_target)s,
%(ch2_result)s,
%(ch2_cq)s,
%(ch3_target)s,
%(ch3_result)s,
%(ch3_cq)s,
%(ch4_target)s,
%(ch4_result)s,
%(ch4_cq)s,
%(filtered_positive)s,
%(filtered_positive_version)s,
%(filtered_positive_timestamp)s,
%(created_at)s,
%(updated_at)s
)
ON DUPLICATE KEY UPDATE
plate_barcode=VALUES(plate_barcode),
coordinate=VALUES(coordinate),
date_tested_string=VALUES(date_tested_string),
date_tested=VALUES(date_tested),
source=VALUES(source),
lab_id=VALUES(lab_id),
created_at=VALUES(created_at),
updated_at=VALUES(updated_at);
"""

SQL_TEST_MLWH_CREATE = """
CREATE DATABASE IF NOT EXISTS `unified_warehouse_test` /*!40100 DEFAULT CHARACTER SET latin1 */;
DROP TABLE IF EXISTS `unified_warehouse_test`.`lighthouse_sample`;
CREATE TABLE `unified_warehouse_test`.`lighthouse_sample` (
`id` int NOT NULL AUTO_INCREMENT,
`mongodb_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Auto-generated id from MongoDB',
`root_sample_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Id for this sample provided by the Lighthouse lab',
`cog_uk_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Consortium-wide id, generated by Sanger on import to LIMS',
`rna_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Lighthouse lab-provided id made up of plate barcode and well',
`plate_barcode` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Barcode of plate sample arrived in, from rna_id',
`coordinate` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Well position from plate sample arrived in, from rna_id',
`result` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Covid-19 test result from the Lighthouse lab',
`date_tested_string` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'When the covid-19 test was carried out by the Lighthouse lab',
`date_tested` datetime DEFAULT NULL COMMENT 'date_tested_string in date format',
`source` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Lighthouse centre that the sample came from',
`lab_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Id of the lab, within the Lighthouse centre',
`ch1_target` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Target for channel 1',
`ch1_result` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Result for channel 1',
`ch1_cq` decimal(11,8) DEFAULT NULL COMMENT 'Cq value for channel 1',
`ch2_target` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Target for channel 2',
`ch2_result` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Result for channel 2',
`ch2_cq` decimal(11,8) DEFAULT NULL COMMENT 'Cq value for channel 2',
`ch3_target` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Target for channel 3',
`ch3_result` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Result for channel 3',
`ch3_cq` decimal(11,8) DEFAULT NULL COMMENT 'Cq value for channel 3',
`ch4_target` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Target for channel 4',
`ch4_result` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Result for channel 4',
`ch4_cq` decimal(11,8) DEFAULT NULL COMMENT 'Cq value for channel 4',
`filtered_positive` boolean DEFAULT NULL COMMENT 'Filtered positive result value',
`filtered_positive_version` varchar(255) DEFAULT NULL COMMENT 'Filtered positive version',
`filtered_positive_timestamp` datetime DEFAULT NULL COMMENT 'Filtered positive timestamp',
`created_at` datetime DEFAULT NULL COMMENT 'When this record was inserted',
`updated_at` datetime DEFAULT NULL COMMENT 'When this record was last updated',
PRIMARY KEY (`id`),
UNIQUE KEY `index_lighthouse_sample_on_root_sample_id_and_rna_id_and_result` (`root_sample_id`,`rna_id`,`result`),
UNIQUE KEY `index_lighthouse_sample_on_mongodb_id` (`mongodb_id`),
KEY `index_lighthouse_sample_on_date_tested` (`date_tested`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

SQL_MLWH_MULTIPLE_FILTERED_POSITIVE_UPDATE = """\
UPDATE lighthouse_sample
SET filtered_positive = %(filtered_positive)s, filtered_positive_version = %(filtered_positive_version)s, filtered_positive_timestamp = %(filtered_positive_timestamp)s
WHERE mongodb_id = %(mongodb_id)s
"""

# DART SQL queries
SQL_DART_GET_PLATE_PROPERTY = """\
SET NOCOUNT ON
DECLARE @output_value nvarchar(256)
EXECUTE [dbo].[plDART_PlatePropGet] @plate_barcode = ?, @prop_name = ?, @value = @output_value OUTPUT
SELECT @output_value
"""

SQL_DART_SET_PLATE_PROPERTY = """\
SET NOCOUNT ON
DECLARE @return_code int
EXECUTE @return_code = [dbo].[plDART_PlatePropSet] @plate_barcode = ?, @prop_name = ?, @prop_value = ?
SELECT @return_code
"""

SQL_DART_GET_PLATE_BARCODES = """\
SELECT DISTINCT [Labware LIMS BARCODE] FROM [dbo].[LIMS_test_plate_status] WHERE [Labware state] = ?
"""
SQL_DART_SET_WELL_PROPERTY ="{CALL dbo.plDART_PlateUpdateWell (?,?,?,?)}"