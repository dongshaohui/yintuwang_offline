# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取拍拍贷投资产品数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.ppdai.com/lend/12_s0_p"
g_product_link = "http://www.ppdai.com"

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

def get_page_num():
	page_link = g_root_link
	r = urllib2.Request(page_link)
	r.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	opener = urllib2.build_opener()
	f= opener.open(r)
	soup = BeautifulSoup(f.read())
	page_num = soup.find('span',{'class':'pagerstatus'}).text
	page_r = re.compile(r'\d+')
	return (int)(re.findall(page_r,page_num)[0])

def fetch_single_data(db,link):
	r = urllib2.Request(link)
	r.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	opener = urllib2.build_opener()
	f= opener.open(r)
	soup = BeautifulSoup(f.read())
	product_list = soup.findAll('tr')[1:]
	for product in product_list:
		record = {}
		record['proName'] = product.findAll('td')[1].find('a').text
		record['urllink'] = g_product_link + product.findAll('td')[1].find('a')['href']
		record['interest'] = product.findAll('td')[3].text
		record['amount'] = product.findAll('td')[4].text.split(';')[1].replace(',','')
		record['duetime'] = product.findAll('td')[5].text
		record['progress'] = product.findAll('td')[6].findAll('p')[-1].text
		progress_r = re.compile(r'\d+')
		record['progress'] = re.findall(progress_r,record['progress'])[0] + "%"
		record['credit'] = product.findAll('td')[0].find('i')['class'].split(' ')[1]
		record['minamount'] = '50'
		record['surplus'] = (float)(record['amount'])*(1.0 - (float)(record['progress'][:-1]) / 100.0)
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_paipaidai_lend')


def fetch_web_data(db):
	page_num = get_page_num()
	for i in range(1,page_num+1):
		page_link = g_root_link + (str)(i)
		fetch_single_data(db,page_link)

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_paipaidai_lend')
	fetch_web_data(db)
