# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取陆金所富盈人生数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import DB

g_root_link = "https://list.lufax.com/list/fuying"
g_pro_link = "https://list.lufax.com/list/productDetail?productId="

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

# 获取产品地址信息
def getProLinks(db):
	curSoup = getSoupFromWeblink(g_root_link)
	proinfos = curSoup.findAll('li',{'class':'product-list clearfix'})
	for i in range(0,len(proinfos)):
		getProDetailInfo(db,proinfos[i])
	proinfos = curSoup.findAll('li',{'class':'product-list clearfix '})
	for i in range(0,len(proinfos)):
		getProDetailInfo(db,proinfos[i])

# 获取产品详情信息
def getProDetailInfo(db,proinfo):
	# 产品详情
	proName = proinfo.find('a').text #　产品名称
	interest_rate_tag = proinfo.find('li',{'class':'interest-rate'})
	proInterest = interest_rate_tag.find('p').text # 产品利率
	period_tag = proinfo.find('li',{'class':'invest-period'})
	proPeriod = period_tag.find('p').text # 产品投资期限
	
	proID = dict(proinfo.find('a').attrs)['data-productid']
	proUrlLink = g_pro_link + proID

	proAmount = proinfo.find('div',{'class':'product-amount is-3rd-col'}).find('em').text
	record_obj = {}
	record_obj['proName'] = proName
	record_obj['proInterest'] = proInterest
	record_obj['proPeriod'] = proPeriod
	record_obj['proAmount'] = proAmount
	record_obj['urllink'] = proUrlLink
	record_obj['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	write_record_db(db,record_obj,'p2p_product_lufax_fuying')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_lufax_fuying')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_lufax_fuying')
	getProLinks(db)
