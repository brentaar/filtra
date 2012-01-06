#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import os
import hashlib
import StringIO
import time
def fileindex():
  for root,dirs,files in os.walk(pytcwd):
    for files in files:
      filespli = os.path.splitext(files)
      #TODO: will need to rewrite, possibly put in def, and find a better way to find the 
      # metadata/extension
      fileex = filespli[1]
      fileex = fileex.strip(".")
      filepath = os.path.join(root,files)
      if not os.path.exists(filepath):
       continue
      filestat = os.stat(filepath)
      filepath = msani(filepath)
      
      #size in bytes
      filesize = filestat.st_size
      q1 = "SELECT id FROM pyth_files WHERE filepath = '%s' " % filepath
      filename = os.path.basename(files)
      filename = msani(filename)
      cur.execute(q1)
      rows = cur.fetchone()     
      if rows < 1:
        q2 = """INSERT INTO pyth_files 
          SET filename = '%s', filepath = '%s', filetype = '%s', fileexist = 1, filesize = '%s' """ % (filename,filepath,fileex,filesize)

        cur.execute(q2)    
    con.commit()

  cur.close()

def msani(v):
  v = v.replace("\'","\\\'")
  v = v.replace("\"","\\\"")  
  return v

def checkexist():
  q1 = "SELECT id,filepath FROM pyth_files WHERE filepath LIKE '%s%%' " % pytcwd
  cur.execute(q1)
  rows = cur.fetchall()
  for row in rows:
    if not os.path.exists(row[1]):
      q2 = "UPDATE pyth_files SET fileexist = 0 WHERE id = '%s' " % row[0]
      cur.execute(q2)
    else:
      q3 = "UPDATE pyth_files SET fileexist = 1 WHERE id = '%s' " % row[0]
      cur.execute(q3)
  
  con.commit()

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size
      
def filehash():

 q0 = "SELECT id,filepath,filesize FROM pyth_files WHERE fileexist = 1 AND filepath LIKE '%s%%' ORDER BY filesize" % pytcwd
 cur.execute(q0) 

 rows = cur.fetchall()
 for row in rows:
  fileid = row[0]
  filepath = row[1]
  filesize = row[2]
  filehash = filemd5(filepath,filesize)
  
  q1 = "SELECT id FROM pyth_hash WHERE hash = '%s' " % filehash
  cur.execute(q1)
  rows1 = cur.fetchone()
  
  if rows1 < 1:
    q2 = "INSERT INTO pyth_hash SET hash = '%s' " % filehash
    cur.execute(q2)
    #con.commit()
    q2a = "INSERT INTO cl_pyth_hashmap SET hashid = '%s',fileid ='%s' " % (con.insert_id(),fileid)
    cur.execute(q2a)
  else:
    hashid = rows1[0]

    q3a = "SELECT id FROM cl_pyth_hashmap WHERE hashid = '%s' AND fileid = '%s' " % (hashid,fileid)
    cur.execute(q3a)
    q3ars = cur.fetchone()
    if q3ars < 0:
      
      q3 = "INSERT INTO cl_pyth_hashmap SET hashid = '%s',fileid ='%s' " % (hashid,fileid)
      cur.execute(q3)
  con.commit()

def filemd5(filepath,filesize):
 readsize = filesize 
 md5 = hashlib.md5()
 try:
  f = open(filepath)
 except IOError as e:
  return 0
 if readsize > 8192:
  while True:
   data = f.read(8192)
   if not data:
    break
   md5.update(data)
 else:
  data = f.read(readsize)
  md5.update(data)
 return md5.hexdigest()

def hashclean():
  q3 = """DELETE FROM cl_pyth_hashmap WHERE fileid IN(
  SELECT id FROM pyth_files WHERE fileexist = 0 AND filepath LIKE '%s%%'
  ) """ % pytcwd
  cur.execute(q3)
  con.commit() 

    
def filedupes():
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
     for var in varArray:
       q3 = "SELECT filepath from pyth_files WHERE id = '%s' " % var
       cur.execute(q3)
       print " %s" % cur.fetchone()

def countDupes():
  count = 0
  q1 = "SELECT fileids,hash FROM pyth_hash WHERE fileids LIKE '%%,%%' "
  cur.execute(q1)
  rows = cur.fetchall()
  for row in rows:
    fids = row[0]
    q2 = "SELECT id FROM pyth_files WHERE id IN(%s) AND filepath LIKE '%s%%' " % (fids,pytcwd)
    cur.execute(q2)
    q2out = cur.fetchone()
    if q2out > 0:
       varArray = fids.split(",")
       count = count + len(varArray) - 1
  print ""
  print "Number of duplicated files %d " % count

#################################################################
start = time.time()
con = None
      
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
  hashclean()
  filehash()
 elif( sys.argv[1] == 'dupes' ):
  
  filedupes()
 elif(sys.argv[1] == 'cdupes' ):
  countDupes()
 else:
  #Write help text
  print "help text"
  
except mdb.Error, e:
 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)

finally:
  if con:    
    con.close()

elapsed = (time.time() - start)

print ""
print "Elapsed %f seconds" % elapsed
print ""

exit()
