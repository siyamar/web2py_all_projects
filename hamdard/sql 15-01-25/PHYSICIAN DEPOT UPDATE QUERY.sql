ALTER TABLE `sm_physician` ADD `gender` VARCHAR(20) NULL DEFAULT '' AFTER `mobile_no`;

ALTER TABLE sm_physician_depot
ADD physician_name varchar(255) DEFAULT NULL;

ALTER TABLE sm_physician_depot
ADD depot_name varchar(255) DEFAULT NULL;


ALTER TABLE sm_physician_depot
MODIFY physician_name varchar(255) AFTER physician_id;

ALTER TABLE sm_physician_depot
MODIFY depot_name varchar(255) AFTER depot_id;
