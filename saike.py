# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time


def sprider_content(headers,url):
	html = requests.get(url,headers=headers).text
	content = etree.HTML(html)
	return content

def judge_update_isContent(old_content,content):
	text_list = content.xpath('//div[@class="fl event4-1-detail-box"]//h3/a/text()')
	new_content = ""
	for text in text_list:
		new_content += text+"\n"
	if(old_content != new_content):
		print "已更新！"
		return new_content
	else:
		print "未更新！"
		return False

def generate_content(content):
	name_list = content.xpath('//div[@class="fl event4-1-detail-box"]//a/@title')
	content_list = content.xpath('//div[@class="fl event4-1-detail-box"]//p[3]/text()')
	url_list = content.xpath('//div[@class="fl event4-1-detail-box"]//a/@href')
	send_string = "最新更新比赛信息："
	for name,content,url in zip(name_list,content_list,url_list):
		string = name.encode('utf-8') + "\n" + "报名时间：" + content.encode('utf-8') + "\n" + "链接地址：" + url.encode('utf-8')
		send_string = send_string + '\n' + '\n' + '\n' + string
	send_string = send_string + '\n' + '\n' + '\n' + "本竞赛信息来源于网络！由翼梦工作室发送！"
	return send_string
def print_nowtime():
	timeInfo = time.localtime( time.time())
	print "当前时间:" + str(timeInfo.tm_year) + "年" + str(timeInfo.tm_mon) + "月" + str(timeInfo.tm_mday) + "日" + str(timeInfo.tm_hour) + ":" + str(timeInfo.tm_min)
	print "\n"
def send_content(send_string):
	mail_host="smtp.163.com"  
	mail_user="leroy_it2@163.com"    
	mail_pass="xwdshtzg812"   
	sender = 'leroy_it2@163.com'
	receivers = ['651350292@qq.com','2472243601@qq.com']  
	message = MIMEText(send_string, 'plain', 'utf-8')
	message['From'] = "朱忠政<leroy_it2@163.com>"
	message['To'] =  "651350292<651350292@qq.com>;2472243601<2472243601@qq.com>"
	subject = '比赛信息'
	message['Subject'] = Header(subject, 'utf-8')
	smtp = smtplib.SMTP()
	smtp.connect(mail_host,25)
	smtp.login(mail_user,mail_pass)  
	smtp.sendmail(sender, receivers, message.as_string())
	print "邮件发送成功!"


def scheduler():
	headers = {"User-Agent" : "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"}
	url = "https://www.saikr.com/vs/0/0/1"
	old_content = ""
	while True:
		content = sprider_content(headers,url)
		judge_result = judge_update_isContent(old_content,content)
		if(judge_result):
			send_string = generate_content(content)
			send_content(send_string)
			old_content = judge_result
			print_nowtime()
		else:
			print_nowtime()
		time.sleep(60*10)

if __name__ == '__main__':
	scheduler()
