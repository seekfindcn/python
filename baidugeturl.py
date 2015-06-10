#!/user/bin/python
import re
import urllib

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html
	
def getTxt(html):
	reg = r"(http://tieba.baidu.com/p/[0-9]\d*)</a>?"
	txtre = re.compile(reg)
	txtlist = re.findall(txtre,html)
	return txtlist

def getTxtHtml(html)

html = getHtml("http://tieba.baidu.com/p/2227314825")
print getTxt(html)