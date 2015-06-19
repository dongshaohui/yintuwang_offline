# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取人人贷Ｕ计划数据
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import DB

g_pro_root_link = "http://www.renrendai.com/financeplan/listPlan!detailPlan.action?financePlanId="

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

# 获取存续期
def getDuetime(urllink):
	soup = getSoupFromWeblink(urllink)
	datestr = soup.find('div',{'class':'fn-left planinfo'}).findAll('dl')[2].find('em').text
	return datestr
	

# 解析Ｕ计划json数据
def parse_uplan_json_link(db,cur_data_link):
	content = urllib2.urlopen(cur_data_link,'r').read()
	json_objs = json.loads(content)
	for json_obj in json_objs["data"]["plans"]:
		record = {}
		record['name'] = json_obj['name']
		record['amount'] = json_obj['amount']
		record['avalibleAmount'] = json_obj['avalibleAmount']
		record['category'] = json_obj['category']
		record['expectedYearRate'] = json_obj['expectedYearRate']
		#record['waitTime'] = json_obj['waitTime']
		record['earnInterest'] = json_obj['earnInterest']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		record['urllink'] = g_pro_root_link + (str)(json_obj['id'])
		record['waitTime'] = getDuetime(record['urllink'])
		if json_obj['status'] == '1' or json_obj['status'] == '4':
			write_record_db(db,record,'p2p_product_renrendai_u_plan')
		else:
			break
	if len(json_objs["data"]["plans"]) == 0:
		return False
	else:
		return True

# 解析Ｕ计划数据
def parse_uplan_data(db,g_link):
	page_index = 1
	while True:
		cur_data_link =	g_link + (str)(page_index)
		if parse_uplan_json_link(db,cur_data_link) == False:
			break
		page_index = page_index + 1

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_renrendai_u_plan')
	#os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_renrendai_u_plan')
	g_uplan_A_data_link = "http://www.renrendai.com/financeplan/listPlan!listPlanJson.action?category=A&pageIndex="
	g_uplan_B_data_link = "http://www.renrendai.com/financeplan/listPlan!listPlanJson.action?category=B&pageIndex="
	g_uplan_C_data_link = "http://www.renrendai.com/financeplan/listPlan!listPlanJson.action?category=C&pageIndex="
	parse_uplan_data(db,g_uplan_A_data_link)
	parse_uplan_data(db,g_uplan_B_data_link)
	parse_uplan_data(db,g_uplan_C_data_link)
