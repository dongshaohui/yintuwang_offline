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

g_root_link = "http://www.yirendai.com/transfer/list/1"
g_transfer_link = "http://www.yirendai.com"

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

def fetch_json_data(db):
	page_link = g_root_link
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=5)
	soup = BeautifulSoup(f.read())
	translist = soup.find('ul',{'class':'bidList transferList'})
	if translist == None:
		return
	prolist = translist.findAll('li',{'class':'clearfix'})
	for product in prolist:
		record = {}
		record['proName'] = product.find('div',{'class':'leftpart'}).find('a').text
		record['recentpay'] = product.find('div',{'class':'leftpart'}).find('div',{'class':'l bidDetail'}).find('span').text
		recent_pay_r = re.compile(r'\d{4}-\d{2}-\d{2}')
		record['recentpay'] = re.findall(recent_pay_r,record['recentpay'])[0]
		record['deadline'] = product.find('div',{'class':'leftpart'}).find('div',{'class':'l bidDetail'}).findAll('p')[-1].text
		deadline_r = re.compile(r'\d+')
		record['deadline'] = '-'.join(re.findall(deadline_r,record['deadline']))  # 天－小时－分钟
		record['surplus'] = product.find('div',{'class':'leftpart'}).find('div',{'class':'l bid_total'}).find('span').text
		record['interest'] = product.find('div',{'class':'leftpart'}).find('div',{'class':'l bid_rate'}).find('span').text + "%"
		record['duetime'] = product.find('div',{'class':'leftpart'}).find('div',{'class':'l bidInfor'}).find('h4').text
		record['urllink'] = g_transfer_link + product.find('div',{'class':'leftpart'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_yirendai_transfer')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_yirendai_transfer')
	fetch_json_data(db)
