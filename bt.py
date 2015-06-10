#!/user/bin/python
# -*- coding: utf-8 -*-
import re
import urllib
import string

class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>|<br>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n    ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:  
            x = x.replace(t[0],t[1])  
        return x  


def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html
	
def getTxt(html):
	reg = r"(http://tieba.baidu.com/p/[0-9]\d*)</a>?"
	txtre = re.compile(reg)
	txtlist = re.findall(txtre,html)
	return txtlist

def getTxtHtml(url):
    # 申明相关的属性
    def __init__(self,url):  
        self.myUrl = url + '?see_lz=1'
        self.datas = []
        self.myTool = HTML_Tool()
        print u'已经启动贴吧爬虫'
	page = urllib.urlopen(url)
	myPage = page.read()
	titleMatch = re.search(r'<h1.*?>(.*?)</h1>', myPage, re.S)
	title = u'暂无标题'
	if myMatch:
		title  = myMatch.group(1)
		print u'正在下载:' + title
	else:
		print u'爬虫报告：无法加载文章标题！'
	data = self.myTool.Replace_Char(title.replace("\n","").encode('gbk'))
	self.datas.append(data+'\n')
	myItems = re.findall('id="post_content.*?>(.*?)</div>',myPage,re.S)
	txtitem = myItems.group(2)
	data = self.myTool.Replace_Char(txtitem.replace("\n","").encode('gbk'))
	self.datas.append(data+'\n')
	f = open('text.txt','a')
	f.writelines(self.datas)
	f.close()
	

#调用
html = getHtml("http://tieba.baidu.com/p/2227314825")
txturllist = getTxt(html)

for bdurl in txturllist:
	getTxtHtml(bdurl)