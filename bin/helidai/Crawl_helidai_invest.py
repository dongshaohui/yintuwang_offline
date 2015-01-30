# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取宜人贷理财服务数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.helloan.cn/process/company/lend/bids"
g_pro_link = "http://www.helloan.cn/process/public/bid/detail/"

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
	product_list = soup.findAll('div',{'class':'bd fixed'})
	for product in product_list:
		progress_digit = product.find('span',{'class':'degital'})
		if progress_digit == None:
			break
		record = {}
		record['proName'] = product.find('div',{'class':'title title_1'}).text
		record['credit'] = product.find('ul').find('em').text
		record['amount'] = product.findAll('ul')[1].findAll('em')[0].text
		record['duetime'] = product.findAll('ul')[1].findAll('em')[1].text
		record['surplus'] = progress_digit.text
		record['progress'] = product.find('div',{'class':'rl_m'}).text
		record['interest'] = product.find('div',{'class':'perc'}).text
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		clickurl = product.find('div',{'class':'h1 fixed'})['onclick']
		record['urllink'] = g_pro_link + clickurl[clickurl.rfind('/')+1:clickurl.rfind('\'')]
		write_record_db(db,record,'p2p_product_helidai_invest')
	

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_helidai_invest')
	fetch_web_data(db)
