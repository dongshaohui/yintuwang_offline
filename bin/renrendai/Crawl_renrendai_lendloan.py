# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取人人贷散标投资列表数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import DB

g_root_link = "http://www.renrendai.com/lend/loanList.action?pageIndex="
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

# 获取原始json数据
def fetch_json_data(db):
	page_index = 1
	while True:
		page_link = g_root_link + (str)(page_index)
		soup = BeautifulSoup(urllib2.urlopen(page_link,'r').read())
		json_content = soup.find('script',{'id':'loan-list-rsp'}).text
		json_objs = json.loads(json_content)
		
		for loan in json_objs['data']['loans']:
			if loan['status'] != 'OPEN':
				return
			else:
				record = {}
				record['title'] = loan['title']
				record['amount'] = loan['amount']
				record['interest'] = (str)(loan['interest']) + "%"
				record['months'] = (str)((int)(loan['months']))
				record['surplusAmount'] = loan['surplusAmount']
				record['finishedRatio'] = (str)(float('%0.2f'%(loan['finishedRatio']))) + "%"
				record['openTime'] = loan['openTime']
				record['startTime'] = loan['startTime']
				record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				record['urllink'] = g_loan_link + (str)((int)(loan['loanId']))
				write_record_db(db,record,'p2p_product_renrendai_lendload')
		page_index += 1

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_renrendai_lendload')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_renrendai_lendload')
	fetch_json_data(db)
