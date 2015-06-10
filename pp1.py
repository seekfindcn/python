# -*- coding: gbk -*-
import os
import sys
import codecs

def convert(file,in_enc="GBK",out_enc="UTF-8"):
	try:
		print ("convert " +file)
		f=codecs.open(file,'r',in_enc)
		new_content=f.read()
		codecs.open(file,'w',out_enc).write(new_content)
		#print (f.read())
	except IOError as err:
		print ("I/O error: {0}".format(err))


def explore(dir):
	for root,dirs,files in os.walk(dir):
		for file in files:
			path=os.path.join(root,file)
			convert(path)

def main():
	for path in sys.argv[1:]:
		if(os.path.isfile(path)):
			convert(path)
		elif os.path.isdir(path):
			explore(path)

	if __name__=="__main__":
		main()  