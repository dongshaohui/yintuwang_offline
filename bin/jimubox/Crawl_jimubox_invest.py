# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取积木盒子理财产品数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB
import HTMLParser

g_root_link = "https://www.jimubox.com/Project/List?status=1&rate=&range=&flag=close"
g_project_link = "https://www.jimubox.com"

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
	f = urllib2.urlopen(r, data=None, timeout=3)
	soup = BeautifulSoup(f.read())
	invest_projects = soup.findAll('div',{'class':'project-item-content'})
	html_parser = HTMLParser.HTMLParser()
	for invest in invest_projects:
		record = {}
		record['proName'] = invest.find('h4',{'class':'project-name'}).find('a').text.replace('&nbsp;','')
		record['proInfo'] = html_parser.unescape(invest.find('p',{'class':'project-info'}).text)
		record['amount'] = invest.findAll('p',{'class':'project-info'})[1].find('span',{'class':'project-sum-money'}).text + "万".decode('utf-8')
		record['curamount'] = (invest.findAll('p',{'class':'project-info'})[1].find('span',{'class':'project-current-money'}).text).replace('/','').replace(' ','').replace('&nbsp;','')
		curamount_r = re.compile(r'\d+')
		curamount_count = re.findall(curamount_r,record['curamount'])
		if len(curamount_count) == 0:
			continue
		record['interest'] = html_parser.unescape(invest.find('div',{'class':'project-other-left'}).find('span').text) + "%"
		record['duetime'] = html_parser.unescape(invest.find('div',{'class':'project-other-right'}).find('span').text) + "月".decode('utf-8')
		record['urllink'] = g_project_link + invest.find('h4',{'class':'project-name'}).find('a')['href']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_record_db(db,record,'p2p_product_jimubox_invest')
 
if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_jimubox_invest')
	fetch_web_data(db)
