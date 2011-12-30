#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import os
import hashlib

con = None

try:

 con = mdb.connect('localhost', 'pyth', 'shafted', 'pyth');
 
 cur = con.cursor()
 cur.execute("SELECT VERSION()")
 
 data = cur.fetchone()
 
 print "Database version : %s " % data
 
 
 pytcwd = os.getcwd()
 
 for root,dirs,files in os.walk(pytcwd):
  for files in files:
   filespli = os.path.splitext(files)
   fileex = filespli[1]
   filepath = os.path.join(root,files)   
   filename = os.path.basename(files)
   cur.execute("INSERT INTO pyth_files SET filename = '%s', filepath = '%s', filetype = '%s', fileexist = 1 " % (filename, filepath,fileex))    

except mdb.Error, e:

 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)

finally:    

 if con:    
  con.close()
