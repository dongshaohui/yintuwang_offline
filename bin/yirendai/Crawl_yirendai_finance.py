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

g_root_link = "http://www.yirendai.com/finance/list/1"
g_loan_link = "http://www.yirendai.com"

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

# 获取理财产品数据
def fetch_json_data(db):
	page_index = 1
	page_link = g_root_link
	soup = BeautifulSoup(urllib2.urlopen(page_link,'r').read())
	# 理财服务
	loans = soup.findAll('div',{'class':'ydy_banner ydy_banner_two clearfix'})
	for loan in loans:
		parse_loan(loan)

# 解析单个标的
def parse_loan(loan):
	record = {}
	record['proName'] = loan.find('div',{'class':'l ydy_logo'}).find('a').text.replace(' ','').replace('\n','')
	amount_r = re.compile(r'\d+.*')
	record['amount'] = re.findall(amount_r,loan.find('div',{'class':'l ydy_logo'}).find('p').text)[0]
	record['interest'] = loan.find('div',{'class':'l numbers'}).find('span',{'class':'percent'}).text
	record['duetime'] = loan.find('div',{'class':'l numbers'}).find('span',{'class':'months'}).text
	record['surplus'] = loan.find('div',{'class':'l amount_countdown'}).find('p',{'class':'surplus_morne'}).find('strong').text.replace(',','')
	record['min_amount'] = loan.find('div',{'class':'l amount_countdown'}).find('input')['value']
	record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	record['urllink'] = g_loan_link + loan.find('div',{'class':'l ydy_logo'}).find('a')['href']
	write_record_db(db,record,'p2p_product_yirendai_finance')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_yirendai_finance')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_yirendai_finance')
	fetch_json_data(db)
