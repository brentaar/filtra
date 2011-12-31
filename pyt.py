#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import os
import hashlib

con = None

def fileindex():
  for root,dirs,files in os.walk(pytcwd):
    for files in files:
      filespli = os.path.splitext(files)
      fileex = filespli[1]
      fileex = fileex.strip(".")
      filepath = os.path.join(root,files)
      filename = os.path.basename(files)
      cur.execute("SELECT * FROM pyth_files WHERE filepath = '%s'" % filepath)
      rows = cur.fetchone()
      
      if rows < 1:     
        cur.execute("INSERT INTO pyth_files SET filename = '%s', filepath = '%s', filetype = '%s', fileexist = 1 " % (filename,filepath,fileex))    
    con.commit()
  cur.close()

def filehash():
  cur.execute("SELECT id,filepath FROM pyth_files WHERE fileexist = 1 AND filepath LIKE '%s%%' " % pytcwd) 
  rows = cur.fetchall()
  for row in rows:
    filehash = filemd5(row[1])
    #print "fh: %s" % filehash
    cur.execute("SELECT fileid,hash FROM pyth_hash WHERE fileid = '%s' " % row[0])
    rows1 = cur.fetchone()
    if rows1 < 1:
      cur.execute("INSERT INTO pyth_hash SET fileid = '%s', hash = '%s' " % (row[0],filehash))
    else:
      cur.execute("UPDATE pyth_hash SET hashstamp = CURRENT_TIMESTAMP WHERE fileid = '%s' " % row[0])
    con.commit()
  cur.close
  
def filemd5(filepath):
 md5 = hashlib.md5()
 f = open(filepath)
 while True:
  data = f.read(8192)
  if not data:
    break
  md5.update(data)
 return md5.hexdigest()
  
def filedupes():
  print "DUPES"
  cur.execute("SELECT fileid,hash FROM pyth_hash WHERE hash IN ( SELECT hash FROM pyth_hash GROUP BY hash HAVING count(hash) > 1 ) ORDER BY hash")
  rows = cur.fetchall()
  hashnumber = None
  for row in rows:
    cur.execute("SELECT filepath from pyth_files WHERE id = '%s' " % row[0])
    out = cur.fetchone()
    tmphash = row[1]
    if hashnumber != tmphash:
      print "HASH: %s" % row[1]
      hashnumber = row[1]
    print " %s " % out
  
  
  ######################
      
if(len(sys.argv) < 2):
  print "help text"
  sys.exit(1)

try:
 
 con = mdb.connect('localhost', 'pyth', 'shafted', 'pyth') 
 cur = con.cursor()
 pytcwd = os.getcwd() 
 if( sys.argv[1] == 'index' ):
  fileindex()
 elif( sys.argv[1] == 'hash' ):
  filehash()
 elif( sys.argv[1] == 'dupes' ):
  filedupes()
 else:
  print "help text"
  
except mdb.Error, e:

 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)

finally:
  if con:    
    con.close()


