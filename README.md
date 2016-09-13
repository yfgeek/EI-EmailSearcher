# EI-EmailSearcher
## 简介
这是一个针对EI学术库的大规模数据采集工具。
## 参数

名称 | 变量 | 作用
-----|------|----
开始号| startnumit| 搜索起始页
截止号| endnum  | 搜索尾页
间隔数| set    | 每发送邮件的间隔数量
邮件名称|mailtit|发送邮件的名称，随意

## Search ID
什么是Search ID？

Search ID是指在http://www.engineeringvillage.com 经过一定网址搜索后，进入检索页面后，随便点入任意检索项的页面地址中的url的SEARCHID=部分。

### 举个栗子
``http://www.engineeringvillage.com/search/doc/abstract.url?pageType=quickSearch&searchtype=Quick&SEARCHID=dec13de6M7267M4879M9c68M2fa04fabf6e1&DOCINDEX=1&database=1&format=quickSearchAbstractFormat&dedupResultCount=1``

中的SEARCHID部分即为``dec13de6M7267M4879M9c68M2fa04fabf6e1``

## 发件
在此处更改发件邮箱、密码、发件服务器
```
  self.from_addr = "test@qq.com"
  self.pwd = "test"          
  self.smtp_server = "smtp.qq.com" 
```
## 储存
每达到间隔数，便会生成`标题-时间.txt`的文件用于储存备份，并以附件的形式发送到邮箱里备份
