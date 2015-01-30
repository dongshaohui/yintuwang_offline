# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 将数据库中所有p2p理财产品数据进行整合
import DB
import os
import sys
sys.path.append('../tool/')
import manipulate_conf
import ConfigParser

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
def db_data_integrate(db):
	cf = ConfigParser.ConfigParser()
	cf.read('../conf/db_field_mapping.ini')
	sections = cf.sections()
	section_map = {}
	for section in sections:
		section_map['product_source'] = section
		options = cf.options(section)
		for option in options:
			element = cf.get(section,option)
			section_map[element] = option
	for section_map_key in section_map:
		print section_map_key,section_map[section_map_key]

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	#os.system(script_path + '  p2p_product_nvg_p2p_product_detail')
	#fetch_web_data(db)
	db_data_integrate(db)
	fetch_table_field_from_db(db,'p2p_product_nvg_p2p_product_detail')
