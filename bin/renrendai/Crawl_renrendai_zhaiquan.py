# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取人人贷债券转让数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import DB

g_root_link = "http://www.renrendai.com/transfer/transferList.action"
g_pro_link = "http://www.renrendai.com/transfer/loanTransferDetail.action?transferId="

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
	soup = BeautifulSoup(urllib2.urlopen(g_root_link ,'r').read())
	json_content = soup.find('script',{'id':'transfer-list-rsp'}).text
	json_objs = json.loads(json_content)
	for transfer_obj in json_objs['data']['transferList']:
		record = {}
		record['title'] = transfer_obj['title']
		record['interest'] = (str)(transfer_obj['interest']) + "%"
		record['leftPhaseCount'] = transfer_obj['leftPhaseCount']
		record['pricePerShare'] = transfer_obj['pricePerShare']
		record['discountRatio'] = transfer_obj['discountRatio']
		record['resultPice'] = transfer_obj['resultPice']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		record['urllink'] = g_pro_link + (str)(transfer_obj['id'])
		write_record_db(db,record,'p2p_product_renrendai_zhaiquan')
		

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_renrendai_zhaiquan')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_renrendai_zhaiquan')
	fetch_json_data(db)
