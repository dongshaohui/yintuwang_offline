# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取爱投资产品

from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import DB

g_root_link = "http://www.itouzi.com/dinvest/ajax/list?type=&status=1"
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
	json_objs = json.loads(soup.text,encoding='utf-8')['data']['borrows']
	for json_obj in json_objs:
		record = {}
		record['proName'] = json_obj['name']
		record['amount'] = (str)((float)(json_obj['accountW']) * 10000)
		record['duetime'] = ((str)(json_obj['timeLimit']) + '个月').decode('utf-8')
		record['interest'] = json_obj['apr'] + '%'
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		record['urllink'] = g_pro_link + json_obj['detailUrl']
		write_record_db(db,record,'p2p_product_itouzi')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_itouzi')
	fetch_web_data(db)
