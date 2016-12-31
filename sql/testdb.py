"""
module that provides connectivity to our local lab database
"""
import os

host = os.environ['DBLOCALHOST']
port = os.environ['DBLOCALPORT']
db = 'bfl'
user = os.environ['DBUSER']
password = os.environ['DBPW']


"""
generic functions used by other *db.py
to connect to databases
"""
import MySQLdb
import MySQLdb.cursors

def conn(h=host,p=port,d=db,u=user,pw=password):
	return MySQLdb.Connect(host=h,port=p,user=u,passwd=pw,db=d)

def dictconn(h=host,p=port,d=db,u=user,pw=password):
	return MySQLdb.Connect(host=h,port=p,user=u,passwd=pw,db=d,
                    cursorclass=MySQLdb.cursors.DictCursor)


