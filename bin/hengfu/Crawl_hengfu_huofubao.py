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
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())
	prolist = soup.find('div',{'class':'biaot_content_2'}).find('table').findAll('tr')
	for product in prolist:
		if product.find('img') != None:
			continue
		proAttrs = product.findAll('td')
		record = {}
		record['proName'] = proAttrs[2].find('a').text
		record['amount'] = proAttrs[3].text
		record['interest'] = proAttrs[4].text
		record['duetime'] = proAttrs[5].text
		record['surplus'] = proAttrs[6].text
		record['minAmount'] = '1'
		record['urllink'] = g_pro_link + proAttrs[2].find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_hengfu_huofubao')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_hengfu_huofubao')
	fetch_web_data(db)

