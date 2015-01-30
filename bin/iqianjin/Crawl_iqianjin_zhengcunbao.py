# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取爱钱进 整存宝p2p理财产品数据

from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.iqianjin.com/plan/lists?pageIndex=0&pageSize=100&pageIndex=0&pageSize=12&_=1420422652671"
g_transfer_link = "http://www.iqianjin.com"

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

def fetch_json_data(db):
	page_link = g_root_link
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=3)
	json_obj_list = json.loads(f.read())['bean']['list']
	for product in json_obj_list:
		if product['status'] != 2:
			continue
		record = {}
		record['proName'] = product['issue'] + '期'.decode('utf-8')
		record['amount'] = product['amount']
		record['minAmount'] = 1000
		record['interest'] = product['avgYieldDesc']
		record['joinerCount'] = product['joinerCount'] # 加入人数
		record['invested'] = product['realAmount']
		record['surplus'] = record['amount'] - record['invested'] 
		record['progress'] = (str)(round((float)(record['invested']) / (float)(record['amount']),3) * 100) + "%"
		record['duetime'] = (str)(product['period']) + "个月".decode('utf-8')
		record['urllink'] = "http://www.iqianjin.com/plan/list"
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_iqianjin_zhengcunbao')




if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_iqianjin_zhengcunbao')
	fetch_json_data(db)
