# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取新联在线p2p理财产品
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "http://www.newunion.cn/finance.do"
g_pro_link = "http://www.newunion.com/"

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
	os.system("DISPLAY=:0 phantomjs " + os.getcwd() + "/get_xinlianzaixian_invest.js > " + os.getcwd() + "/xinlianzaixian.temp" )
	f = open(os.getcwd()+'/xinlianzaixian.temp','r')
	soup = BeautifulSoup(f.read())
	f.close()
	prolist1 = soup.findAll('div',{'class':'i_new_project_c_list'})
	prolist2 = soup.findAll('div',{'class':'i_new_project_c_list active'})
	prolist = prolist1 + prolist2 
	for product in prolist:
		record = {}
		record['guarantor'] = product.find('li',{'class':'w360'}).find('div',{'class':'i_new_project_c_list_bq t_l'}).find('img')['title']
		record['proName'] = product.find('div',{'class':'i_new_project_c_list_title fl t_l  lh69 f_16 w250'}).find('a')['title']
		record['interest'] = product.find('li',{'class':'w106'}).find('span').text + "%"
		record['amount'] = product.find('li',{'class':'w176'}).find('span').text
		amount_r = re.compile(r'\d+\.?\d*')
		amount_digit = re.findall(amount_r,record['amount'])
		record['amount'] = "".join(amount_digit)
		record['minAmount'] = 50
		duetime_spans = product.find('li',{'class':'w78 lh69'}).findAll('span')
		duetime_span_texts = map(lambda x:x.text, duetime_spans)
		record['duetime'] = "".join(duetime_span_texts)
		record['progress'] = product.find('li',{'class':'w130'}).find('em').text
		progress_r = re.compile(r'\d+\.?\d*')
		progress_digit = re.findall(progress_r,record['progress'])[0]
		record['surplus'] = (float)(record['amount']) * (100.0 - (float)(progress_digit)) / 100.0
		record['urllink'] = g_pro_link + product.find('li',{'class':'w360'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_xinlianzaixian_invest')
		

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + ' p2p_product_xinlianzaixian_invest')
	fetch_web_data(db)
