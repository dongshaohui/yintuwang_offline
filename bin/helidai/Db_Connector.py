#!/usr/bin/python  
# -*- coding:utf-8 -*-
# Author: Dong Shaohui
# Desc: Connect To DB ops
# Date: 2014-12-18
import ConfigParser
import DB

class Db_Connector:
	def __init__(self, config_file_path):
		cf = ConfigParser.ConfigParser()
		cf.read(config_file_path)
		self.host = cf.get('db','host')
		self.port = cf.get('db','port')
		self.user = cf.get('db','user')
		self.pwd = cf.get('db','password')
		self.dbname = cf.get('db','dbname')
		self.db = self.Connent_Online_Mysql_By_DB('jsfundb0qu.mysql.rds.aliyuncs.com',3306,'market_7778','AAaa1234','hexun-fund-market','/tmp/mysql.sock')

	def Connent_Online_Mysql_By_DB(self,hostname,port,username,pwd,dbname,socket):
		try:
			db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
		except Exception,e:
			print "Exception"
		return db
	
	def getDBInstance(self):
		return self.db

