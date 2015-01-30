# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取91旺财理财产品数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.91wangcai.com/list"
g_pro_link = "http://www.91wangcai.com"

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
	f = urllib2.urlopen(r, data=None, timeout=5)
	soup = BeautifulSoup(f.read())
	prolist = soup.findAll('div',{'class':'product clearfix pro_c0'})
	for product in prolist:
		record = {}
		record['proName'] = product.find('a').text
		record['interest'] = product.find('li',{'class':'con first'}).find('em').text
		record['duetime'] = product.findAll('li',{'class':'con'})[0].find('em').text
		record['amount'] = product.findAll('li',{'class':'con'})[1].find('em').text
		record['minAmount'] = 100
		record['investLimit'] = product.find('li',{'class':'end'}).find('em').text # 投资限额
		record['surplus'] = product.find('div',{'class':'per'}).find('em').text
		record['urllink'] = g_pro_link + product.find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_91wangcai_invest')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_91wangcai_invest')
	fetch_web_data(db)
