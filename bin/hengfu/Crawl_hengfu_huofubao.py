# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取活富宝数据(恒富天下)
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://www.hengfu100.com/productHQBList"
g_pro_link = "https://www.hengfu100.com/"

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
	print page_link
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())
	prolist = soup.find('div',{'class':'layout fix H-container'}).findAll('div',{'class':'fix product-Li huafb-Li'})
	for product in prolist:
		if product.find('div',{'class':'fl pro-active'}).find('a')['class'] != 'btn1':
			break
		record = {}
		record['proName'] = product.find('a').text
		record['amount'] = product.find('ul').findAll('li')[2].find('span').text.replace(',','')
		record['interest'] = product.find('ul').findAll('li')[0].find('span').text
		record['duetime'] = product.find('ul').findAll('li')[1].find('span').text
		record['surplus'] = product.find('ul').findAll('li')[3].find('span').text.replace(',','')
		record['minAmount'] = '1'
		record['urllink'] = g_pro_link + product.find('div',{'class':'fl pro-active'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_hengfu_huofubao')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_hengfu_huofubao')
	# os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_hengfu_huofubao')
	fetch_web_data(db)

