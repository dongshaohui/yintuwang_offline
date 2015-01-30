# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取陆金所稳盈-安e数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import DB

g_page_link = "https://list.lufax.com/list/anyi?currentPage="
g_root_link = "https://list.lufax.com/list/anyi"
g_pro_root_link = "https://list.lufax.com"

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

# 获取页数
def getPageNumber():
	soup = getSoupFromWeblink(g_root_link)
	page_number_tag = soup.findAll('a',{'class':'btns btn_page btn_small last'})[0]['data-val']
	return (int)(page_number_tag)

# 获取产品地址列表
def getProLink(db):
	pageNum = getPageNumber()
	plist = []
	for i in range(0,pageNum):
		curlink = g_page_link + (str)(i+1)
		curSoup = getSoupFromWeblink(curlink)
		statusinfos = curSoup.findAll('div',{'class':'progress-wrap clearfix'})
		proinfos = curSoup.findAll('li',{'class':'product-list  clearfix '})
		amountinfos = curSoup.findAll('div',{'class':'product-amount'})
		for i in range(0,len(proinfos)):
			getProDetail(db,proinfos[i],statusinfos[i],amountinfos[i])

# 获取单个产品详情
def getProDetail(db,proinfo,statusinfo,amountinfo):
	# 产品状态
	proProgress = statusinfo.find('span').text

	# 产品详情
	proName = proinfo.find('a').text # 产品名称
	interest_rate_tag = proinfo.find('li',{'class':'interest-rate'})
	proInterest = interest_rate_tag.find('p').text # 产品利率
	period_tag = proinfo.find('li',{'class':'invest-period'})
	proPeriod = period_tag.find('p').text # 产品投资期限
	remain_capital = proinfo.find('li',{'class':'collection-mode'}).find('em').text # 剩余资金
	proUrlLink = g_pro_root_link + dict(proinfo.find('a').attrs)['href']

	# 起投资金详情
	proAmount = amountinfo.find('em').text
	record_obj = {}
	record_obj['proName'] = proName
	record_obj['proInterest'] = proInterest
	record_obj['proAmount'] = proAmount
	record_obj['proPeriod'] = proPeriod
	record_obj['proProgress'] = proProgress
	record_obj['remain_capital'] = remain_capital
	record_obj['urllink'] = proUrlLink
	record_obj['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	write_record_db(db,record_obj,'p2p_product_lufax_anyi')


if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_lufax_anyi')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_lufax_anyi')
	getProLink(db)
