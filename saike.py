# -*- coding: UTF-8 -*-
import requests     
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
old_string = ""
headers = {"User-Agent" : "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"} #IE报头
url = "https://www.saikr.com/vs/0/0/1" #塞克url
while  True:
	html = requests.get(url,headers=headers).text
	content = etree.HTML(html)
	text_list = content.xpath('//div[@class="fl event4-1-detail-box"]//h3/a/text()')
	new_string = ""
	for text in text_list:
		new_string += text+"\n"
	if(old_string != new_string):
		mail_host="smtp.163.com"  #设置服务器
   		mail_user="leroy_it2@163.com"    #用户名
   		mail_pass="xwdshtzg812"   #口令 
		sender = 'leroy_it2@163.com'
		receivers = ['651350292@qq.com']  # 接收邮件地址
   		message = MIMEText(new_string, 'plain', 'utf-8')
   		message['From'] = "朱忠政<leroy_it2@163.com>"
   		message['To'] =  "651350292<651350292@qq.com>"
   		subject = '比赛信息'
   		message['Subject'] = Header(subject, 'utf-8')
		smtp = smtplib.SMTP()
		smtp.connect(mail_host,25)    # 25 为 SMTP 端口号
		smtp.login(mail_user,mail_pass)  
		smtp.sendmail(sender, receivers, message.as_string())
		print "邮件发送成功"
		old_string = new_string
		time.sleep(60*60)
