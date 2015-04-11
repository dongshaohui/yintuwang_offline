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
g_transfer_link = "http://www.jinhaidai.com"

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
	product_list = soup.findAll('div',{'class':'project-content-div'})
	for product in product_list:
		if product.find('div',{'class':'right invest-button'}).find('a')['class'] != 'btn-invest btn btn-orange':
			continue
		record = {}
		record['proName'] = product.find('a').text
		record['urllink'] = g_transfer_link + product.find('a')['href']
		record['amount'] = product.find('div',{'class':'left amount'}).find('p').text[1:]
		record['minAmount'] = '1000'
		record['duetime'] = product.find('div',{'class':'left limit'}).find('p').text
		record['interest'] = product.find('div',{'class':'left rate'}).find('div').text
		record['progress'] = product.find('div',{'class':'progress-bgPic'}).find('div').text
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_jinhaidai_borrow')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_jinhaidai_borrow')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_yirendai_transfer')
	fetch_web_data(db)
