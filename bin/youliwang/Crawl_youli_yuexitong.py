# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取有利网月息通数据
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

def fetch_web_data(db,pagetag):
	#os.system("DISPLAY=:0 phantomjs " + os.getcwd() + "/get_youli_dingcunbao.js > " + os.getcwd() + "/dingcunbao.temp" )
	f = open(os.getcwd()+'/tmp_page'+(str)(pagetag) + '.tmp','r')
	soup = BeautifulSoup(f.read())
	f.close()
	prolist = soup.findAll('ul',{'class':'items'})
	for product in prolist:
		linktag = product.find('li',{'class':'col_7'}).find('a')
		if linktag == None:
			return False
		record = {}
		record['proName'] = product.find('li',{'class':'col_1'}).find('a').text
		record['interest'] = product.find('li',{'class':'col_2'}).text
		record['amount'] = product.find('li',{'class':'col_3'}).text
		amount_r = re.compile(r'\d+')
		record['amount'] = "".join(re.findall(amount_r,record['amount']))
		record['duetime'] = product.find('li',{'class':'col_4'}).text
		record['guarantor'] = product.find('li',{'class':'col_5'}).text
		record['progress'] = product.find('li',{'class':'col_6'}).text
		progress_r = re.compile(r'\d+')
		progress_digit = (float)(re.findall(progress_r,record['progress'])[0]) / 100.0
		record['surplus'] = progress_digit * (int)(record['amount'])
		record['minAmount'] = '50'
		record['urllink'] = g_pro_link + product.find('li',{'class':'col_1'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_youliwang_yuexitong')
	return True
	
if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + ' p2p_product_youliwang_yuexitong')
	for i in range(1,4):
		if fetch_web_data(db,i) == False:
			break
	os.system('rm -rf *.tmp')
