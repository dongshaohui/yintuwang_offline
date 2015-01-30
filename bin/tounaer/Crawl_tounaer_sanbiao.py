# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取投哪儿网散标理财数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.touna.cn/borrow.do?method=list&borrowType=0&creditType=&timeLimit=&keyType=0&page=0&size=10&subtime=1419922895125&_=1419922895126"
g_pro_link = "http://www.touna.cn/invest-page.html?id="

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
	context = urllib2.urlopen(g_root_link,'r').read()
	json_obj = json.loads(context)
	for product in json_obj['result']['list']:
		if product['status'] != 1:
			continue
		record = {}
		record['proName'] = product['name']
		record['amount'] = product['account']
		record['interest'] = product['apr']
		record['invested'] = product['account_yes']
		record['surplus'] = (float)(record['amount']) - (float)(record['invested'])
		record['credit'] = product['credit_rating']
		record['duetime'] = product['time_limit_name']
		record['status'] = product['status_name']
		record['pubtime'] = product['pubtime']
		record['minamount'] = '50'
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		record['urllink'] = g_pro_link + (str)(product['id'])
		write_record_db(db,record,'p2p_product_tounaer_sanbiao')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_tounaer_sanbiao')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_tounaer_sanbiao')
	fetch_json_data(db)
