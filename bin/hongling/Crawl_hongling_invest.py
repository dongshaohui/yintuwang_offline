# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取红岭创投投资列表数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import DB
import re

g_root_link = "https://www.my089.com/Loan/"
g_page_index_link = "https://www.my089.com/Loan/default.aspx?pid="
g_loan_link = "http://www.renrendai.com/lend/detailPage.action?loanId="
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

# 获取页数
def fetch_page_number():
	soup = BeautifulSoup(urllib2.urlopen(g_root_link,'r').read())
	page_tag = soup.find('div',{'class':'yema rt'}).find('span',{'class':'z_page'}).text
	page_r = re.compile(r'\d+')
	return (int)(re.findall(page_r,page_tag)[0])

def fetch_web_data(db):
	page_n = fetch_page_number()
	for i in range(1,page_n+1):
		page_link = g_page_index_link + str(i)
		soup = BeautifulSoup(urllib2.urlopen(page_link,'r').read())
		loanlist = soup.findAll('dl',{'class':'LoanList'})
		for loan in loanlist:
			record = {}
			record['proName'] = loan.find('div',{'class':'txt_tou'}).find('a')['title']
			record['loanType'] = loan.find('div',{'class':'txt_tou'}).find('b')['class']
			record['interest'] = loan.find('dd',{'class':'dd_2 mar_top_18'}).text
			record['amount'] = loan.find('dd',{'class':'dd_3 mar_top_18'}).text
			record['duetime'] = loan.find('dd',{'class':'dd_4 mar_top_18'}).text.split('/')[0].replace(' ','')
			record['paytype'] = loan.find('dd',{'class':'dd_4 mar_top_18'}).text.split('/')[1].replace(' ','')
			record['progress'] = loan.find('dd',{'class':'dd_6 mar_top_18'}).find('span').text
			record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			record['urllink'] = g_root_link + loan.find('div',{'class':'txt_tou'}).find('a')['href']
			progress_r = re.compile(r'\d+')
			progress_d = (int)(re.findall(progress_r,record['progress'])[0])
			if progress_d < 100:
				write_record_db(db,record,'p2p_product_hongling_loan')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_hongling_loan')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_hongling_loan')
	fetch_web_data(db)
