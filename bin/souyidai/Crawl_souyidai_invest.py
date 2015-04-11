# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取搜易贷投资理财产品

from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://www.souyidai.com/invest/"
g_pro_link = "https://www.souyidai.com"

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
	prolist = soup.findAll('div',{'class':'version-item version-mb10'})
	for product in prolist:
		record = {}
		record['proName'] = product.find('div',{'class':'ver-top'}).find('a').text
		record['amount'] = product.find('div',{'class':'version-infor-list ver-border-right col-w159'}).find('span',{'class':'version-num'}).text.replace(',','')
		record['minAmount'] = 1
		record['interest'] = product.find('div',{'class':'version-infor cf'}).find('span').text
		record['guarantor'] = product.find('div',{'class':'version-infor-list ver-border-right col-w179'}).find('strong').text
		record['duetime'] = product.find('div',{'class':'version-infor-list ver-border-right col-w99'}).find('span',{'class':'version-num'}).text + "月".decode('utf-8')
		record['paytype'] = product.find('div',{'class':'version-infor-list col-w115'}).find('span',{'class':'version-text lt'}).text
		record['progress'] = product.find('div',{'class':'ver-cls-w77 relative'}).find('span').text + "%"
		record['surplus'] = product.find('div',{'class':'ver-invest-money'}).find('span').text
		surplus_r = re.compile(r'\d+.*')
		record['surplus'] = re.findall(surplus_r,record['surplus'])[0].replace(',','')
		record['urllink'] = g_pro_link + product.find('div',{'class':'ver-top'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_souyidai_invest')
	

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_souyidai_invest')
	fetch_web_data(db)
