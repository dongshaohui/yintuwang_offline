# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 将数据库中所有p2p理财产品数据进行整合,定期整合一次
import DB
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")) + '/tool/')
import manipulate_conf
import ConfigParser
from ConfigParser import ConfigParser
import MySQLdb
import MySQLdb.cursors

class MyConfigParser(ConfigParser):
	def __init__(self):
		ConfigParser.__init__(self)
	def optionxform(self, optionstr):
		return optionstr


# 连接数据库 
def Connent_Online_Mysql_By_DB(hostname,port,username,pwd,dbname,socket):
    db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
    return db

# 写入数据库
def write_record_db(db,list_obj,table_name):
    try:
        db.insert(table_name,list_obj)
        db.commit()
    except Exception,e:
		print e

# 获取数据库表字段数据
def fetch_table_field_from_db(db,table_name):
	fetch_sql = 'describe ' + table_name
	records = db.select(fetch_sql)
	record_list = map(lambda x:(str)(x[0]),records)
	return record_list

# 数据库数据进行整合
def db_data_integrate(db,db1):
	cf = MyConfigParser()
	cf.read(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")) + '/conf/db_field_mapping.ini')
	sections = cf.sections()
	section_map = {}
	query_db = MySQLdb.connect(host='rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',user='dongsh',passwd='5561225',db='financal_product',charset="utf8",cursorclass=MySQLdb.cursors.DictCursor)
	cursor = query_db.cursor()
	for section in sections:
		section_map[section] = {} 
		options = cf.options(section)
		for option in options:
			element = cf.get(section,option)
			section_map[section][option] = element
	for key in section_map:
		tablename = section_map[key]['tablename']
		cursor.execute('select * from ' + tablename);
		product_result = cursor.fetchall()
		for product_record in product_result:
			record = {}
			for subkey in section_map[key]:
				if subkey == 'tablename':
					continue
				sub_element = section_map[key][subkey]
				record[sub_element] = product_record[subkey]
			write_record_db(db1,record,'p2p_products')
if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	db1 = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','wangdai_p2p','/tmp/mysql.sock')
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	db_data_integrate(db,db1)
	#fetch_table_field_from_db(db,'p2p_product_nvg_p2p_product_detail')
