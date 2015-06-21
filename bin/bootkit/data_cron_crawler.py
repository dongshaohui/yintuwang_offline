# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 开启定期抓取数据脚本
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/tool/')
import ConfigParser
from ConfigParser import ConfigParser
import MySQLdb
import MySQLdb.cursors
import datetime


starttime = datetime.datetime.now()

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# 91旺财 91wangcai
os.system('python ' + script_path + '/91wangcai/Crawl_91wangcai_invest.py')
print "91旺财 finish"
# 合力贷 helidai
os.system('python ' + script_path + '/helidai/Crawl_helidai_invest.py')
print "合力贷 finish"
# 恒富天下 hengfu
os.system('python ' + script_path + '/hengfu/Crawl_hengfu_hengfubao.py')
os.system('python ' + script_path + '/hengfu/Crawl_hengfu_huofubao.py')
print "恒富天下 finish"
# 红岭创投 hongling 
os.system('python ' + script_path + '/hongling/Crawl_hongling_invest.py')
print "红岭创投 finish"
# 爱钱进 iqianjin
os.system('python ' + script_path + '/iqianjin/Crawl_iqianjin_lingqiantong.py')
os.system('python ' + script_path + '/iqianjin/Crawl_iqianjin_zhengcunbao.py')
print "爱钱进 finish"
# 爱投资 itouzi
os.system('python ' + script_path + '/itouzi/Crawl_itouzi.py')
# os.system('python ' + script_path + '/itouzi/Crawl_itouzi_aibaoli.py')
# os.system('python ' + script_path + '/itouzi/Crawl_itouzi_aidanbao.py')
# os.system('python ' + script_path + '/itouzi/Crawl_itouzi_dept.py')
print "爱投资 finish"
# 积木盒子 jimubox
os.system('python ' + script_path + '/jimubox/Crawl_jimubox_invest.py')
print "积木盒子 finish"
# 金海贷 jinhaidai
os.system('python ' + script_path + '/jinhaidai/Crawl_jinhaidai_invest.py')
print "金海贷 finish"
# 陆金所 lufax
os.system('python ' + script_path + '/lufax/Crawl_lufax_anyi.py')
os.system('python ' + script_path + '/lufax/Crawl_lufax_fuying.py')
os.system('python ' + script_path + '/lufax/Crawl_lufax_zhuanxiang.py')
os.system('python ' + script_path + '/lufax/Crawl_lufax_zhujiang.py')
print "陆金所 finish"
# 你我贷 niwodai
os.system('python ' + script_path + '/niwodai/Crawl_niwodai_loan.py')
print "你我贷 finish"
# 拍拍贷 paipaidai
os.system('python ' + script_path + '/paipaidai/Crawl_paipaidai_lend.py')
print "拍拍贷 finish"
# 人人贷 renrendai
os.system('python ' + script_path + '/renrendai/Crawl_renrendai_lendloan.py')
os.system('python ' + script_path + '/renrendai/Crawl_renrendai_u_plan.py')
os.system('python ' + script_path + '/renrendai/Crawl_renrendai_zhaiquan.py')
print "人人贷 finish"
# 搜易贷 souyidai
os.system('python ' + script_path + '/souyidai/Crawl_souyidai_invest.py')
print "搜易贷 finish"
# 投哪儿网 tounaer
os.system('python ' + script_path + '/tounaer/Crawl_tounaer_guonianbao.py')
os.system('python ' + script_path + '/tounaer/Crawl_tounaer_sanbiao.py')
print "投哪儿网 finish"
# 网信理财 wangxinlicai
os.system('python ' + script_path + '/wangxinlicai/Crawl_wangxinlicai_invest.py')
print "网信理财 finish"
# 新联在线 xinlianzaixian
os.system('python ' + script_path + '/xinlianzaixian/Crawl_xinlianzaixian_invest.py')
print "新联在线 finish"
# 银湖网 yinhu
os.system('python ' + script_path + '/yinhu/Crawl_yinhu_loan.py')
print "银湖网 finish"
# 宜人贷 yirendai
os.system('python ' + script_path + '/yirendai/Crawl_yirendai_finance.py')
os.system('python ' + script_path + '/yirendai/Crawl_yirendai_loan.py')
os.system('python ' + script_path + '/yirendai/Crawl_yirendai_transfer.py')
print "宜人贷 finish"
# 有利网 youliwang (使用phantomjs)

# 所有数据整合
script_path = os.getcwd()
os.system('python ' + script_path + '/db_data_integration.py')

endtime = datetime.datetime.now()
print (endtime - starttime).seconds
