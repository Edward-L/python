#coding:utf-8
import re 
import requests

#get html
r = requests.get('http://www.edwardl.xyz')
data = r.text
##data1 = r.headers
#print data1
#use re to find all url 
link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
for url in link_list:
	print url