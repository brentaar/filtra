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
  `fileids` text NOT NULL,
  `hashstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


