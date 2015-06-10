# -*- coding: utf8 -*-
#
# 将txt小说分割转换成多个HTML文件
#
# @author : GreatGhoul
# @email  : greatghoul@gmail.com
# @blog   : http://greatghoul.iteye.com

import re
import os
# import codecs

# regex for the section title
# sec_re = re.compile(r'第.+卷\s+.+\s+第.+章\s+.+')

# txt book's path.
source_path = 'd:\\tie.txt'

path_pieces = os.path.split(source_path)
novel_title = re.sub(r'(\..*$)|($)', '', path_pieces[1])
target_path = '%s%s_html' % (path_pieces[0], novel_title)
section_re = re.compile(r'^第[0-9一二三四五六七八九十百千零]{1,20}章+.*$')
#"第(一|二|三|四|五|六|七|八|九|十|百|[0-9])+(章)", "i") or re:test(., "序\s", "i")
section_head = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" xmlns:xml="http://www.w3.org/XML/1998/namespace">
<head>
<title>%s</title>
<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head>
<body>
<h3>%s</h3>'''

# escape xml/html
def escape_xml(code):
    text = code
    text = re.sub(r'<', '&lt;', text)
    text = re.sub(r'>', '&gt;', text)
    text = re.sub(r'&', '&amp;', text)
    text = re.sub(r'\t', '&nbsp;&nbsp;&nbsp;&nbsp;', text)
    text = re.sub(r'\s', '', text)
    return text

# entry of the script
def main():
    # create the output folder
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    # open the source file
    input = open(source_path, 'r')

    sec_count = 0
    sec_cache = []
    idx_cache = []

    output = open('%s\\%d.html' % (target_path, sec_count), 'w')
    preface_title = '%s 简介' % novel_title
    output.writelines([section_head % (preface_title, preface_title)])
    idx_cache.append('<li><a href="%d.html">%s</a></li>'
                     % (sec_count, novel_title))
        
    for line in input:
        # is a chapter's title?
        if line.strip() == '':
            pass
        elif re.match(section_re, line):
            line = re.sub(r'\s+', ' ', line)
            print 'converting %s...' % line

            # write the section footer
            # sec_cache.append('<hr/><p>')
            # if sec_count == 0:
                # sec_cache.append('<a href="index.html">目录</a>&nbsp;|&nbsp;')
                # sec_cache.append('<a href="%d.html">下一篇</a>&nbsp;|&nbsp;'
                                 # % (sec_count + 1))
            # else:
                # sec_cache.append('<a href="%d.html">上一篇</a>&nbsp;|&nbsp;'
                                 # % (sec_count - 1))
                # sec_cache.append('<a href="index.html">目录</a>&nbsp;|&nbsp;')
                # sec_cache.append('<a href="%d.html">下一篇</a>&nbsp;|&nbsp;'
                                 # % (sec_count + 1))
            # sec_cache.append('<a name="bottom" href="#">回页首</a></p>')
            sec_cache.append('</body></html>')
            output.writelines(sec_cache)
            output.flush()
            output.close()
            sec_cache = []
            sec_count += 1

            # create a new section
            output = open('%s\\%d.html' % (target_path, sec_count), 'w')
            output.writelines([section_head % (line, line)])
            idx_cache.append('<li><a href="%d.html">%s</a></li>'
                             % (sec_count, line))
        else:
            sec_cache.append('<p>%s</p>'
                             % escape_xml(line))
            
    # write rest lines
    # sec_cache.append('<a href="%d.html">下一篇</a>&nbsp;|&nbsp;'
                     # % (sec_count - 1))
    # sec_cache.append('<a href="index.html">目录</a>&nbsp;|&nbsp;')
    # sec_cache.append('<a name="bottom" href="#">回页首</a></p></body></html>')
    sec_cache.append('</body></html>')
    output.writelines(sec_cache)
    output.flush()
    output.close()
	
    sec_cache = []

    # write the menu
    output = open('%s\\index.html' % (target_path), 'w')
    # output.write(codecs.BOM_UTF8)
    menu_head = '%s 目录' % novel_title
    output.writeline([section_head % (menu_head, menu_head), '<ul style="text-align:left">'])
    output.writeline(idx_cache )
    output.writeline(['</ul><body></html>'])
    output.flush()
    output.close()
    inx_cache = []
    
    print 'completed. %d chapter(s) in total.' % sec_count

if __name__ == '__main__':
    main()