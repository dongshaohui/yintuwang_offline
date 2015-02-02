# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取宜人贷精英标数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.yirendai.com/loan/list/"
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

def fetch_json_data(db):
	page_index = 1
	while True:
		page_link = g_root_link + (str)(page_index)
		soup = BeautifulSoup(urllib2.urlopen(page_link,'r').read())
		loans = soup.find('ul',{'class':'bidList'}).findAll('li',{'class':'clearfix'})
		for loan in loans:
			if parse_loan(loan) == False:
				return
		page_index += 1
	
# 解析单个标的
def parse_loan(loan):
	parse_result = False
	loan_detail = loan.find('div',{'class':'loan_detail'})
	if None == loan_detail.find('div',{'class':'rightpart'}).find('div',{'class':'bidForm bidForm_full'}):
		record = {}
		record['proName'] = loan_detail.find('div',{'class':'leftpart'}).find('a').text
		record['urllink'] = g_loan_link + loan_detail.find('div',{'class':'leftpart'}).find('a')['href']
		record['loaned'] = loan_detail.find('div',{'class':'l bidDetail'}).find('p').text
		loaned_r = re.compile(r'\d+')
		record['loaned'] = re.findall(loaned_r,record['loaned'])[-1]
		record['amount'] = loan_detail.find('div',{'class':'l bid_total'}).find('span').text.replace(',','').encode('utf-8')
		record['surplus'] = (int)(record['amount']) - (int)(record['loaned'])
		record['progress'] = (str)(float('%0.3f'%((float)(record['loaned']) / (float)(record['amount'])))*100) + "%"
		record['interest'] = loan_detail.find('div',{'class':'l bid_rate'}).find('span').text + "%"
		record['duetime'] = loan_detail.find('div',{'class':'l bidInfor'}).find('h4').text
		record['unit'] = loan_detail.find('div',{'class':'bidForm'}).find('input')['value']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_yirendai_loan')
		return True
	else:
		return False

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + ' p2p_product_yirendai_loan')
	fetch_json_data(db)
