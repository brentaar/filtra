CREATE TABLE `pyth_files` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `filename` text,
  `filepath` text,
  `filetype` text DEFAULT NULL,
  `fileexist` tinyint DEFAULT 0,
  `filestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `filesize`  bigint(20),
  INDEX (`filesize`),
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

