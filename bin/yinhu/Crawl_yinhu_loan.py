# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取银湖网理财服务数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://www.yinhu.com/loan/loan_list.bl"
g_pro_link = "https://www.yinhu.com"

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
	for product in soup.find('div',{'id':'loan_list'}).find('tbody').findAll('tr'):
		record = {}
		record['progress'] = product.find('span',{'class':'pst_num_r'}).text
		if (float)(record['progress'][:-1]) == 100:
			continue
		record['proName'] = product.find('a').text
		record['credit'] = product.find('td',{'class':'tx_stl16'}).text
		record['interest'] = product.findAll('td')[2].text # 银湖网有活动优惠 +1%的收益率
		interest_r = re.compile(r'\d+\.?\d+')
		interest_digit_list = re.findall(interest_r,record['interest'])
		interest_digit = sum(map(lambda x: (float)(x), interest_digit_list))
		record['interest'] = (str)(round(interest_digit,3)) + "%"
		record['amount'] = product.findAll('td')[3].text.replace(',','')
		amount_r = re.compile(r'\d+')
		record['amount'] = re.findall(amount_r,record['amount'])[0]
		progress_r = re.compile(r'\d+\.?\d*')
		progress_digit = re.findall(progress_r,record['progress'])[0]
		record['surplus'] = (100.0 - (float)(progress_digit)) * (float)(record['amount']) / 100.0
		record['minAmount'] = 100
		record['duetime'] = product.findAll('td')[4].text
		record['urllink'] = g_pro_link + product.find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_yinhu_loan')
	

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_yinhu_loan')
	fetch_web_data(db)
