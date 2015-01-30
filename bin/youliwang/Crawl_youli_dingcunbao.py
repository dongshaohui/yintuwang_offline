# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取有利网定存宝数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.yooli.com/dingcunbao/"
g_pro_link = "http://www.yooli.com"

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
	os.system("DISPLAY=:0 phantomjs " + os.getcwd() + "/get_youli_dingcunbao.js > " + os.getcwd() + "/dingcunbao.temp" )
	f = open(os.getcwd()+'/dingcunbao.temp','r')
	soup = BeautifulSoup(f.read())
	f.close()
	prolist = soup.findAll('div',{'class':'invest-v vdcb'})
	for product in prolist:
		linktag = product.find('a',{'class':'gbtn'})
		if linktag == None:
			continue
		record = {}
		record['proName'] = product.find('li',{'class':'col_1'}).find('a').text
		record['interest'] = product.find('li',{'class':'col_2'}).text
		record['duetime'] = product.find('li',{'class':'col_3'}).text
		record['progress'] = product.find('li',{'class':'col_5'}).text
		record['surplus'] = product.find('li',{'class':'col_6'}).text
		surplus_r = re.compile(r'\d+')
		record['surplus'] = "".join(re.findall(surplus_r,product.find('li',{'class':'col_6'}).text))
		record['minAmount'] = '1000'
		record['urllink'] = g_pro_link + product.find('li',{'class':'col_7'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_youliwang_dingcunbao')

	
if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + ' p2p_product_youliwang_dingcunbao')
	fetch_web_data(db)
