#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import os
import hashlib
import StringIO

con = None

def fileindex():
  for root,dirs,files in os.walk(pytcwd):
    for files in files:
      filespli = os.path.splitext(files)
      #TODO: will need to rewrite, possibly put in def, and find a better way to find the 
      # metadata/extension
      fileex = filespli[1]
      fileex = fileex.strip(".")
      filepath = os.path.join(root,files)
      filepath = msani(filepath)
      q1 = "SELECT * FROM pyth_files WHERE filepath = '%s' " % filepath
      filename = os.path.basename(files)
      filename = msani(filename)
      cur.execute(q1)
      rows = cur.fetchone()
      
      if rows < 1:
        q2 = "INSERT INTO pyth_files SET filename = '%s', filepath = '%s', filetype = '%s', fileexist = 1 " % (filename,filepath,fileex)
        cur.execute(q2)    
    con.commit()

  cur.close()

def msani(v):
  v = v.replace("\'","\\\'")  
  return v

def checkexist():
  q3 = "SELECT id,filepath FROM pyth_files WHERE filepath LIKE '%s%%' " % pytcwd
  cur.execute(q3)
  rows = cur.fetchall()
  for row in rows:
    if not os.path.exists(row[1]):
      q4 = "UPDATE pyth_file SET fileexist = 0 WHERE id = '%s' " % row[0]
      cur.execute(q4)
  con.commit()
  
def filehash():
 cur.execute("SELECT id,filepath FROM pyth_files WHERE fileexist = 1 AND filepath LIKE '%s%%' " % pytcwd) 
 rows = cur.fetchall()
 for row in rows:
  fileid = row[0]
  filepath = row[1]
  filehash = filemd5(filepath)
  
  q1 = "SELECT id,fileids FROM pyth_hash WHERE hash = '%s' " % filehash
  cur.execute(q1)
  rows1 = cur.fetchone()
  
  if rows1 < 1:
    q2 = "INSERT INTO pyth_hash SET fileids = '%s', hash = '%s' " % (fileid,filehash)
    cur.execute(q2)
  else:
    hashid = rows1[0]
    fileids = rows1[1]
    strfileid = str(fileid)
    ff = str(fileids).find(strfileid)
    if ff < 0:
      newfileids = "%s,%s" % (fileids,strfileid)
      q3 = "UPDATE pyth_hash SET fileids = '%s', hashstamp = CURRENT_TIMESTAMP WHERE id = '%s' " % (newfileids,hashid)
      cur.execute(q3)
  
  
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

def arFind(var,varArray):
  for tmp in varArray:
    if var == tmp:
      return 1
  return 0

def filedupes():
  #TODO: only output if at least one of the files is in the CWD
  q1 = "SELECT fileids,hash FROM pyth_hash WHERE fileids LIKE '%%,%%' "
  cur.execute(q1)
  rows = cur.fetchall()
  for row in rows:
    fids = row[0]
    q2 = "SELECT * FROM pyth_files WHERE id IN(%s) AND filepath LIKE '%s%%' " % (fids,pytcwd)
    cur.execute(q2)
    q2out = cur.fetchone()
    if q2out > 0:
     print "++++++++++++++++++++++++++++++++++++++++++++"
     print "HASH: %s" % row[1]
     varArray = fids.split(",")
     outputstr = None
     for var in varArray:
       q3 = "SELECT filepath from pyth_files WHERE id = '%s' " % var
       cur.execute(q3)
       print " %s" % cur.fetchone()
  
  ######################
      
if(len(sys.argv) < 2):
  print "help text"
  sys.exit(1)

try:
 
 con = mdb.connect('localhost', 'pyth', 'shafted', 'pyth') 
 cur = con.cursor()
 pytcwd = os.getcwd() 
 if( sys.argv[1] == 'index' ):
  checkexist()
  fileindex()
 elif( sys.argv[1] == 'hash' ):
  #clean fileids if file does not exist
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


