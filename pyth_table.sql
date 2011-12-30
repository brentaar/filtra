CREATE TABLE IF NOT EXISTS pyth_files( 
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  filename TEXT,
  filepath TEXT,
  filetype VARCHAR(20),
  fileexist BINARY
  );
CREATE TABLE IF NOT EXISTS pyth_hash(
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  fileid BIGINT,
  hash VARCHAR(50),
  hashdate DATE
  );
  