# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取金海贷理财产品数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://www.jinhaidai.com/borrow/"
g_transfer_link = "http://www.yirendai.com"

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

def fetch_web_data(db):
	page_link = g_root_link
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=3)
	soup = BeautifulSoup(f.read())
	product_list = soup.find('table',{'class':'table table-horizontal'}).findAll('tr')[1:]
	for product in product_list:
		record = {}
		record['proName'] = product.find('a').text.encode('utf-8')
		print record['proName']

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_yirendai_transfer')
	fetch_web_data(db)
