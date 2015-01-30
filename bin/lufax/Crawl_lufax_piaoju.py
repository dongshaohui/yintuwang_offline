# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取陆金所票据数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import DB

g_root_link = "https://list.lufax.com/list/piaoju"

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


# 获取网页的soup信息
def getSoupFromWeblink(urllink):
	content = urllib2.urlopen(urllink).read()
	soup = BeautifulSoup(content)
	return soup

# 获取产品详情信息
def getProDetailInfo(db):
	soup = getSoupFromWeblink(g_root_link)
	print soup

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	getProDetailInfo(db)
