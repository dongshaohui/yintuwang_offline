# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取你我贷债权列表数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://member.niwodai.com/loan/loan.do?totalCount=365&pageNo="
g_transfer_link = "https://member.niwodai.com"
g_default_page_n = 5

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

def fetch_web_data(db,page_tag):
	page_link = g_root_link + (str)(page_tag)
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=3)
	soup = BeautifulSoup(f.read())
	prolist = soup.find('div',{'class':'biaoList'}).findAll('tr')
	for i in range(1,len(prolist)):
		product = prolist[i]
		record = {}
		record['proName'] = product.find('i')['title'] + "-" +  product.find('td')['title']
		record['interest'] = product.find('em',{'class':'fc_orange fs_16'}).text
		record['amount'] = product.find('td',{'class':'j'}).find('em').text.replace(',','')
		record['progress'] = product.find('td',{'class':'fc_3a'}).text
		record['surplus'] = (float)(record['amount']) * (1 - (float)(record['progress'][:-1]) / 100.0)
		record['duetime'] = product.findAll('td')[2].text
		record['urllink'] = g_transfer_link + product.find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_niwodai_loan')
	
if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_niwodai_loan')
	for i in range(1,g_default_page_n+1):
		fetch_web_data(db,i)

