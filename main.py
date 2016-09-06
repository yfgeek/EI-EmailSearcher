#-*- coding: utf-8 -*-
import os
import smtplib
import re
import sys, urllib, urllib2, json,time
import smtplib
import time
import threading

import email.MIMEMultipart
import email.MIMEBase
import os.path  
import mimetypes  

from time import strftime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Data(object):
 #初始化
 def __init__(self,urlf,urlb):
  super(Data, self).__init__()
  self.urlf = urlf
  self.urlb = urlb

 def __format_addr(self,s):
  name, addr = parseaddr(s)
  return formataddr((\
  Header(name, 'utf-8').encode(), \
  addr.encode('utf-8') if isinstance(addr, unicode) else addr))

 def SetMail(self,title,to_addr):
  self.from_addr = "test@qq.com"
  self.pwd = "test"          
  self.smtp_server = "smtp.qq.com"        
  self.title = title
  self.to_addr = to_addr 
  self.filename = ""

 def __SendSSLEmail(self,con,lastcon):
  finalc = con + "<br/><b>" + lastcon + "</b><br />"
  msg = MIMEText(finalc, 'html', 'utf-8')
  msg['From'] = self.__format_addr(u'您的小助手 <%s>' % self.from_addr)
  msg['To'] = self.__format_addr(u'谢老板 <%s>' % self.pwd)
  msg['Subject'] = Header(self.title, 'utf-8').encode()
  server = smtplib.SMTP_SSL(self.smtp_server, 465)
  #server.set_debuglevel(1)
  server.login(self.from_addr, self.pwd)
  try:
   server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
  finally:
   server.quit()
  print ">发送了一封邮件\n"

 def __SendAttachment(self,j):
  main_msg = email.MIMEMultipart.MIMEMultipart()  
  text_msg = email.MIMEText.MIMEText("下载附件就好啦~~~",_charset="utf-8")  
  main_msg.attach(text_msg)
  contype = 'text/plain'  
  maintype, subtype = contype.split('/', 1)
  data = open(self.filename, 'rb')  
  file_msg = email.MIMEBase.MIMEBase(maintype, subtype)  
  file_msg.set_payload(data.read())  
  data.close()  
  email.Encoders.encode_base64(file_msg)   
  basename = os.path.basename(self.filename)  
  file_msg.add_header('Content-Disposition','attachment', filename = basename)
  main_msg.attach(file_msg)  
  main_msg['From'] = self.__format_addr(u'您的小助手 <%s>' % self.from_addr)  
  main_msg['To'] = self.__format_addr(u'谢老板 <%s>' % self.pwd)
  server = smtplib.SMTP_SSL(self.smtp_server, 465)
  server.login(self.from_addr, self.pwd)  
  main_msg['Subject'] = "第" +j+ "次附件备份：" + self.filename
  fullText = main_msg.as_string()
  try:
   server.sendmail(self.from_addr, [self.to_addr], fullText)
  finally:
   server.quit()
  print ">发送了一份附件\n"

 def __SaveTXT(self,con,stauts):
   self.filename = self.title + time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".txt"
   output = open(self.filename, stauts)
   output.write(con)
   output.close()
   print ">输出了一个文件：" + self.filename

 def __get_url_content(self,url):
  geturl = url
  i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Referer": 'http://www.baidu.com'}
  req = urllib2.Request(geturl, headers=i_headers)
  try:
   print "获取网页数据中..."
   ress = urllib2.urlopen(req).read()
   return ress
  except:
   pass
   print "刚刚出错啦~重试中~"
   self.__get_url_content(geturl)
        
 def __getInfo(self,html):
  get = re.compile('<a.*?href="mailto:(.*?)".*?>',re.S)
  result = re.findall(get,html)
  return result

 def __getPIX(self,mailaddress):
  selectit = re.compile('(.*?)@.*?',re.S)
  result = re.findall(selectit,mailaddress)
  return result

 def getEndnum(self):
  print "请稍等..正在获取总数..."
  url = "http://www.engineeringvillage.com/search/doc/abstract.url?" + self.urlf + "1" + self.urlb
  html = self.__get_url_content(url)
  selectit = re.compile('<b>.*?of(.*?).*?',re.S)
  result = re.findall(selectit,html)
  print "总数：" + str(result)
  return result

 def run(self,startnum,num,setnum):
  ct = 0
  sum = 0
  sumtmp = 0
  jt = 1
  self.title = self.title + " 开始于" + str(startnum) + "号"
  setnum = setnum -1
  self.__SendSSLEmail(self.urlf,"老板，我要开始工作啦！")
  con = ""
  lastcon = ""
  print "请等待..."
  for i in range(startnum, num):
   try:
    url = "http://www.engineeringvillage.com/search/doc/abstract.url?" + self.urlf + str(i) + self.urlb
    html = self.__get_url_content(url)
    mailaddress = self.__getInfo(html)
    for j in mailaddress:
     finalcon = ""
     mailpix = ''.join(self.__getPIX(j))
     finalcon = "\"" + mailpix + "\"" + "<" + j + ">;"
     print finalcon
     con = con + finalcon
     ct = ct + 1
     sum = sum + 1
     # sumtmp = sumtmp + 1
     # if (sumtmp > 10):
     #  self.__SendAttachment(jt)
     #  jt =jt +1
     #  sumtmp = 0
     #  self.__SaveTXT('','w')
     print "已完成" + str(i) + "/" + str(num) + "，共有" + str(sum) + "个邮箱\n"
     print "当前已处理" + str(ct) + "条邮箱地址，等待发送中...\n"
     if (ct > setnum):
      lastcon = "<br / >共" + str(ct) + "条邮箱地址，截止到：" + str(i)
      self.__SendSSLEmail(con,lastcon)
      self.__SaveTXT(con,'a')
      con = ""
      ct = 0
   except(TypeError, IndexError):
    pass
  self.__SendSSLEmail(con,"这是最后一份，请检查是不是有重复的~")
  self.__SendAttachment("Last")
  print "已完成" + str(num) + "/" + str(num)
  self.__SendSSLEmail("没啥内容","老板，全都完成啦！")
  print "完成啦"

class Search(object):
 def __init__(self,keyword1,keyword2,startyear,endyear):
  super(Data, self).__init__()
  self.urlf = urlf
  self.urlb = urlb

 # def getSearchID(self):
 #  print "请输入您要搜索的关键字.."
 #  searchparams = {'ecmsfrom': '','enews': 'login','username': self.name,'password':self.password,'lifetime':'0','ecmsfrom':'..%2Fmember%2Fcp%2F'}
 #  str(raw_input("请输入截止号："))

if __name__ == '__main__':

  searchid = raw_input("请输入Search ID：")
  # searchid = "dec13de6M7267M4879M9c68M2fa04fabf6e1"
  urlf = "pageType=quickSearch&searchtype=Quick&SEARCHID=" + searchid + "&DOCINDEX="
  urlb = "&database=1&format=quickSearchAbstractFormat&dedupResultCount="
  computing = Data(urlf,urlb)
  startnumit = raw_input("请输入开始号：")
  # computing.getEndnum()
  endnum = str(raw_input("请输入截止号："))
  set = int(raw_input("间隔数："))
  mailtit = raw_input("请输入邮件名称：")
  computing.SetMail(mailtit,"test@qq.com")
  computing.run(int(startnumit),int(endnum),set)
