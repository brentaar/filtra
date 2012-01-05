CREATE TABLE `pyth_files` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `filename` text,
  `filepath` text,
  `filetype` varchar(20) DEFAULT NULL,
  `fileexist` binary(1) DEFAULT NULL,
  `filestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `filesize`  varchar(20),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `pyth_hash` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `hash` varchar(32) NOT NULL DEFAULT '',
  `hashstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cl_pyth_hashmap` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `hashid` int NOT NULL ,
  `fileid` int NOT NULL,
  primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
