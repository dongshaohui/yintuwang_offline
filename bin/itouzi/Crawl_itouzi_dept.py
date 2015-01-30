# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取爱投资爱保理产品数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.itouzi.com/dinvest/factoring/index?status=1"
g_pro_link = "https://www.itouzi.com"

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
	product_list = soup.findAll('ul',{'class':'invest-product-case-list mtn btn clearfix '})
	for product in product_list:
		record = {}
		record['proName'] = product.find('a').text
		record['guarantee'] = product.find('span',{'class':'i-p-c-l-i-guarantee'}).find('a').findAll('span')[-1].text
		record['minamount'] = '100'
		record['amount'] = product.find('span',{'class':'i-p-c-l-i-financing'}).text
		amount_r = re.compile(r'\d+')
		amount_digit = re.findall(amount_r,record['amount'])[0]
		record['amount'] = record['amount'][record['amount'].find(amount_digit):]
		record['repaytype'] = product.find('span',{'class':'i-p-c-l-i-repayment'}).text
		record['duetime'] = product.find('span',{'class':'i-p-c-l-i-deadline tips'}).text
		duetime_r = re.compile(r'\d+')
		duetime_digit = re.findall(duetime_r,record['duetime'])[0]
		record['duetime'] = record['duetime'][record['duetime'].find(duetime_digit):]
		record['interest'] = product.find('span',{'class':'i-p-c-l-i-earnings'}).text
		interest_r = re.compile(r'\d+')
		interest_digit = re.findall(interest_r,record['interest'])[0]
		record['interest'] = record['interest'][record['interest'].find(interest_digit):]
		record['progress'] = product.find('div',{'class':'i-p-c-s-detail'}).find('span',{'class':'fl fs-s'}).text
		record['surplus'] = product.find('span',{'class':'i-p-c-l-i-need'}).text
		surplus_r = re.compile(r'\d+')
		surplus_digit = re.findall(surplus_r,record['surplus'])
		record['surplus'] = "".join(surplus_digit)
		record['urllink'] = g_pro_link + product.find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_itouzi_aibaoli')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_itouzi_aibaoli')
	fetch_web_data(db)
