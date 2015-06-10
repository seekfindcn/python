#!/usr/bin/env  python
# -*- coding: utf-8 -*-
__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal <kovid at kovidgoyal.net>'
'''
nytimes.com
'''
import re, string, time
from calibre import entity_to_unicode, strftime
from calibre.web.feeds.recipes import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup, Tag, NavigableString, Comment, BeautifulStoneSoup

class NYTimes(BasicNewsRecipe):

    # set headlinesOnly to True for the headlines-only version
    headlinesOnly = False

    # includeSections: List of sections to include. If empty, all sections found will be included.
    # Otherwise, only the sections named will be included. For example,
    #
    #    includeSections = ['Politics','Sports']
    #
    # would cause only the Politics and Sports sections to be included.
    
    includeSections = []  # by default, all sections included

    # excludeSections: List of sections to exclude. If empty, all sections found will be included.
    # Otherwise, the sections named will be excluded. For example,
    #
    #    excludeSections = ['Politics','Sports']
    #
    # would cause the Politics and Sports sections to be excluded. This parameter can be used
    # in conjuction with includeSections although in most cases using one or the other, but
    # not both, is sufficient.
    
    excludeSections = []

    # one_picture_per_article specifies that calibre should only use the first image
    # from an article (if one exists).  If one_picture_per_article = True, the image
    # will be moved to a location between the headline and the byline.
    # If one_picture_per_article = False, all images from the article will be included
    
    # and shown in their original location.
    one_picture_per_article = True

    # The maximum number of articles that will be downloaded
    max_articles_per_feed = 100

    
    if headlinesOnly:
        title='New York Times Headlines'
        description = 'Headlines from the New York Times'        
    else:
        title='New York Times'
        description = 'Today\'s New York Times'
        
    __author__  = 'GRiker/Kovid Goyal/Nick Redding'
    language = 'en'
    requires_version = (0, 7, 5)


    timefmt = ''
    needs_subscription = True
    masthead_url = 'http://graphics8.nytimes.com/images/misc/nytlogo379x64.gif'
    cover_margins = (18,18,'grey99')

    remove_tags_before = dict(id='article')
    remove_tags_after  = dict(id='article')
    remove_tags = [dict(attrs={'class':[
                            'articleFooter',
                            'articleTools',
                            'columnGroup doubleRule',
                            'columnGroup singleRule',
                            'columnGroup last',
                            'columnGroup  last',
                            'doubleRule',
                            'dottedLine',
                            'entry-meta',
                            'entry-response module',
                            'icon enlargeThis',
                            'leftNavTabs',
                            'metaFootnote',
                            'module box nav',
                            'nextArticleLink',
                            'nextArticleLink clearfix',
                            'post-tools',
                            'relatedSearchesModule',
                            'side_tool',
                            'singleAd',
                            re.compile('^subNavigation'),
                            re.compile('^leaderboard'),
                            re.compile('^module'),
                            ]}),
                   dict(id=[
                            'adxLeaderboard',
                            'adxSponLink',
                            'archive',
                            'articleExtras',
                            'articleInline',
                            'blog_sidebar',
                            'businessSearchBar',
                            'cCol',
                            'entertainmentSearchBar',
                            'footer',
                            'header',
                            'header_search',
                            'inlineBox',
                            'login',
                            'masthead',
                            'masthead-nav',
                            'memberTools',
                            'navigation',
                            'portfolioInline',
                            'readerReviews',
                            'readerReviewsCount',
                            'relatedArticles',
                            'relatedTopics',
                            'respond',
                            'side_search',
                            'side_index',
                            'side_tool',
                            'toolsRight',
                            ]),
                   dict(name=['script', 'noscript', 'style','form','hr'])]
    no_stylesheets = True
    extra_css = '''
                .articleHeadline { text-align: left; margin-top:0.5em; margin-bottom:0.25em; }
                .credit { text-align: right; font-size: small; line-height:1em; margin-top:5px; margin-left:0; margin-right:0; margin-bottom: 0; }
                .byline { text-align: left; font-size: small; line-height:1em; margin-top:10px; margin-left:0; margin-right:0; margin-bottom: 0; }
                .dateline { text-align: left; font-size: small; line-height:1em;margin-top:5px; margin-left:0; margin-right:0; margin-bottom: 0; }
                .kicker { font-size: small; line-height:1em;margin-top:5px; margin-left:0; margin-right:0; margin-bottom: 0; }
                .timestamp { text-align: left; font-size: small; }
                .caption { font-size: small; font-style:italic; line-height:1em; margin-top:5px; margin-left:0; margin-right:0; margin-bottom: 0; }
                a:link {text-decoration: none; }
                .articleBody { }
                .authorId {text-align: left; }
                .image {text-align: center;}
                .source {text-align: left; }'''

    def filter_ans(self, ans) :
        total_article_count = 0
        idx = 0
        idx_max = len(ans)-1
        while idx <= idx_max:
            if self.includeSections != []:
                if ans[idx][0] not in self.includeSections:
                    print "SECTION NOT INCLUDED: ",ans[idx][0]
                    del ans[idx]
                    idx_max = idx_max-1
                    continue
            if ans[idx][0] in self.excludeSections:
                print "SECTION EXCLUDED: ",ans[idx][0]
                del ans[idx]
                idx_max = idx_max-1
                continue
            if self.verbose:
                self.log("Section %s: %d articles" % (ans[idx][0], len(ans[idx][1])) )
            for article in ans[idx][1]:
                total_article_count += 1
                if self.verbose:
                    self.log("\t%-40.40s... \t%-60.60s..." % (article['title'].encode('cp1252','replace'),
                              article['url'].encode('cp1252','replace')))
            idx = idx+1
                        
        self.log( "Queued %d articles" % total_article_count )
        return ans

    def fixChars(self,string):
        # Replace lsquo (\x91)
        fixed = re.sub("\x91","��",string)

        # Replace rsquo (\x92)
        fixed = re.sub("\x92","��",fixed)

        # Replace ldquo (\x93)
        fixed = re.sub("\x93","��",fixed)

        # Replace rdquo (\x94)
        fixed = re.sub("\x94","��",fixed)

        # Replace ndash (\x96)
        fixed = re.sub("\x96","�C",fixed)

        # Replace mdash (\x97)
        fixed = re.sub("\x97","��",fixed)

        return fixed

    def get_browser(self):
        br = BasicNewsRecipe.get_browser()
        if self.username is not None and self.password is not None:
            br.open('http://www.nytimes.com/auth/login')
            br.select_form(name='login')
            br['USERID']   = self.username
            br['PASSWORD'] = self.password
            raw = br.submit().read()
            if 'Please try again' in raw:
                raise Exception('Your username and password are incorrect')
        return br

    def skip_ad_pages(self, soup):
        # Skip ad pages served before actual article
        skip_tag = soup.find(True, {'name':'skip'})
        if skip_tag is not None:
            self.log.warn("Found forwarding link: %s" % skip_tag.parent['href'])
            url = 'http://www.nytimes.com' + re.sub(r'\?.*', '', skip_tag.parent['href'])
            url += '?pagewanted=all'
            self.log.warn("Skipping ad to article at '%s'" % url)
            return self.index_to_soup(url, raw=True)

    def get_cover_url(self):
        cover = None
        st = time.localtime()
        year = str(st.tm_year)
        month = "%.2d" % st.tm_mon
        day = "%.2d" % st.tm_mday
        cover = 'http://graphics8.nytimes.com/images/' + year + '/' +  month +'/' + day +'/nytfrontpage/scan.jpg'
        br = BasicNewsRecipe.get_browser()
        try:
            br.open(cover)
        except:
            self.log("\nCover unavailable")
            cover = None
        return cover

    def short_title(self):
        return self.title

    def index_to_soup(self, url_or_raw, raw=False):
        '''
        OVERRIDE of class method
        deals with various page encodings between index and articles
        '''
        def get_the_soup(docEncoding, url_or_raw, raw=False) :
            if re.match(r'\w+://', url_or_raw):
                f = self.browser.open(url_or_raw)
                _raw = f.read()
                f.close()
                if not _raw:
                    raise RuntimeError('Could not fetch index from %s'%url_or_raw)
            else:
                _raw = url_or_raw
            if raw:
                return _raw

            if not isinstance(_raw, unicode) and self.encoding:
                _raw = _raw.decode(docEncoding, 'replace')
            massage = list(BeautifulSoup.MARKUP_MASSAGE)
            massage.append((re.compile(r'&(\S+?);'), lambda match: entity_to_unicode(match, encoding=self.encoding)))
            return BeautifulSoup(_raw, markupMassage=massage)

        # Entry point
        print "index_to_soup()"
        soup = get_the_soup( self.encoding, url_or_raw )
        contentType = soup.find(True,attrs={'http-equiv':'Content-Type'})
        docEncoding =  str(contentType)[str(contentType).find('charset=') + len('charset='):str(contentType).rfind('"')]
        if docEncoding == '' :
            docEncoding = self.encoding

        if self.verbose > 2:
            self.log( "  document encoding: '%s'" % docEncoding)
        if docEncoding != self.encoding :
            soup = get_the_soup(docEncoding, url_or_raw)

        return soup

    def massageNCXText(self, description):
        # Kindle TOC descriptions won't render certain characters
        if description:
            massaged = unicode(BeautifulStoneSoup(description, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
            # Replace '&' with '&'
            massaged = re.sub("&","&", massaged)
            return self.fixChars(massaged)
        else:
            return description

    def parse_todays_index(self):

        def feed_title(div):
            return ''.join(div.findAll(text=True, recursive=True)).strip()

        articles = {}
        key = None
        ans = []
        url_list = []

        def handle_article(div):
            a = div.find('a', href=True)
            if not a:
                return
            url = re.sub(r'\?.*', '', a['href'])
            if not url.startswith("http"):
                return
            if not url.endswith(".html"):
                return
            if 'podcast' in url:
                return
            if '/video/' in url:
                return
            url += '?pagewanted=all'
            if url in url_list:
                return
            url_list.append(url)
            title = self.tag_to_string(a, use_alt=True).strip()
            description = ''
            pubdate = strftime('%a, %d %b')
            summary = div.find(True, attrs={'class':'summary'})
            if summary:
                description = self.tag_to_string(summary, use_alt=False)
            author = ''
            authorAttribution = div.find(True, attrs={'class':'byline'})
            if authorAttribution:
                author = self.tag_to_string(authorAttribution, use_alt=False)
            else:
                authorAttribution = div.find(True, attrs={'class':'byline'})
                if authorAttribution:
                    author = self.tag_to_string(authorAttribution, use_alt=False)
            feed = key if key is not None else 'Uncategorized'
            if not articles.has_key(feed):
                ans.append(feed)
                articles[feed] = []
            articles[feed].append(
                            dict(title=title, url=url, date=pubdate,
                                description=description, author=author,
                                content=''))


        soup = self.index_to_soup('http://www.nytimes.com/pages/todayspaper/index.html')


        # Find each article
        for div in soup.findAll(True,
            attrs={'class':['section-headline', 'story', 'story headline','sectionHeader','headlinesOnly multiline flush']}):

            if div['class'] in ['section-headline','sectionHeader']:
                key = string.capwords(feed_title(div))
                key = key.replace('Op-ed','Op-Ed')
                key = key.replace('U.s.','U.S.')
            elif div['class'] in ['story', 'story headline'] :
                handle_article(div)
            elif div['class'] == 'headlinesOnly multiline flush':
                for lidiv in div.findAll('li'):
                    handle_article(lidiv)
                    
        ans = [(key, articles[key]) for key in ans if articles.has_key(key)]
        return self.filter_ans(ans)

    def parse_headline_index(self):
        
        articles = {}
        ans = []
        url_list = []

        soup = self.index_to_soup('http://www.nytimes.com/pages/todaysheadlines/')

        # Fetch the content table
        content_table = soup.find('table',{'id':'content'})
        if content_table is None:
            self.log("FATAL ERROR: CANNOT FIND CONTENT TABLE")
            return None
        
        # Within this table are <td id=".*Column.*"> entries, each containing one or more h6 tags which represent sections

        for td_col in content_table.findAll('td', {'id' : re.compile('Column')}):
            for div_sec in td_col.findAll('div',recursive=False):
                for h6_sec_name in div_sec.findAll('h6',{'style' : re.compile('text-transform: *uppercase')}):
                    section_name = self.tag_to_string(h6_sec_name,use_alt=False)
                    section_name = re.sub(r'^ *$','',section_name)
                    if section_name == '':
                        continue
                    section_name=string.capwords(section_name)
                    if section_name == 'U.s.':
                       section_name = 'U.S.'
                    elif section_name == 'Op-ed':
                       section_name = 'Op-Ed'
                    pubdate = strftime('%a, %d %b')
                
                    search_div = div_sec
                    for next_tag in h6_sec_name.findNextSiblings(True):
                        if next_tag.__class__.__name__ == 'Tag':
                            if next_tag.name == 'div':
                                search_div = next_tag
                            break
                        
                    # Get the articles
                    for h3_item in search_div.findAll('h3'):
                        byline = h3_item.h6
                        if byline is not None:
                            author = self.tag_to_string(byline,usa_alt=False)
                        else:
                            author = ''
                        a = h3_item.find('a', href=True)
                        if not a:
                            continue
                        url = re.sub(r'\?.*', '', a['href'])
                        if not url.startswith("http"):
                            continue
                        if not url.endswith(".html"):
                            continue
                        if 'podcast' in url:
                            continue
                        if 'video' in url:
                            continue
                        url += '?pagewanted=all'
                        if url in url_list:
                            continue
                        url_list.append(url)
                        self.log("URL %s" % url)
                        title = self.tag_to_string(a, use_alt=True).strip()
                        desc = h3_item.find('p')
                        if desc is not None:
                            description = self.tag_to_string(desc,use_alt=False)
                        else:
                            description = ''
                        if not articles.has_key(section_name):
                            ans.append(section_name)
                            articles[section_name] = []
                        articles[section_name].append(dict(title=title, url=url, date=pubdate, description=description, author=author, content=''))
                     

        ans = [(key, articles[key]) for key in ans if articles.has_key(key)]
        return self.filter_ans(ans)

    def parse_index(self):
        if self.headlinesOnly:
            return self.parse_headline_index()
        else:
            return self.parse_todays_index()
            
    def strip_anchors(self,soup):
        paras = soup.findAll(True)
        for para in paras:
            aTags = para.findAll('a')
            for a in aTags:
                if a.img is None:
                    a.replaceWith(a.renderContents().decode('cp1252','replace'))
        return soup


    def preprocess_html(self, soup):

        kicker_tag = soup.find(attrs={'class':'kicker'})
        if kicker_tag: # remove Op_Ed author head shots
            tagline = self.tag_to_string(kicker_tag)
            if tagline=='Op-Ed Columnist':
                img_div = soup.find('div','inlineImage module')
                if img_div:
                    img_div.extract()
        return self.strip_anchors(soup)

    def postprocess_html(self,soup, True):

        if self.one_picture_per_article:
            # Remove all images after first
            largeImg = soup.find(True, {'class':'articleSpanImage'})
            inlineImgs = soup.findAll(True, {'class':'inlineImage module'})
            if largeImg:
                for inlineImg in inlineImgs:
                    inlineImg.extract()
            else:
                if inlineImgs:
                    firstImg = inlineImgs[0]
                    for inlineImg in inlineImgs[1:]:
                        inlineImg.extract()
                    # Move firstImg before article body
                    article_body = soup.find(True, {'id':'articleBody'})
                    cgFirst = soup.find(True, {'class':re.compile('columnGroup  *first')})
                    if cgFirst:
                        # Strip all sibling NavigableStrings: noise
                        navstrings = cgFirst.findAll(text=True, recursive=False)
                        [ns.extract() for ns in navstrings]
                        headline_found = False
                        tag = cgFirst.find(True)
                        insertLoc = 0
                        while True:
                            insertLoc += 1
                            if hasattr(tag,'class') and tag['class'] == 'articleHeadline':
                                    headline_found = True
                                    break
                            tag = tag.nextSibling
                            if not tag:
                                headline_found = False
                                break
                        if headline_found:
                            cgFirst.insert(insertLoc,firstImg)
                    else:
                        self.log(">>> No class:'columnGroup first' found <<<")

        # Change captions to italic 
        for caption in soup.findAll(True, {'class':'caption'}) :
            if caption and caption.contents[0]:
                cTag = Tag(soup, "p", [("class", "caption")])
                c = self.fixChars(self.tag_to_string(caption,use_alt=False)).strip()
                mp_off = c.find("More Photos")
                if mp_off >= 0:
                    c = c[:mp_off]
                cTag.insert(0, c)
                caption.replaceWith(cTag)

        # Change <nyt_headline> to <h2>
        h1 = soup.find('h1')
        if h1:
            headline = h1.find("nyt_headline")
            if headline:
                tag = Tag(soup, "h2")
                tag['class'] = "headline"
                tag.insert(0, self.fixChars(headline.contents[0]))
                h1.replaceWith(tag)
        else:
            # Blog entry - replace headline, remove <hr> tags
            headline = soup.find('title')
            if headline:
                tag = Tag(soup, "h2")
                tag['class'] = "headline"
                tag.insert(0, self.fixChars(headline.contents[0]))
                soup.insert(0, tag)
                hrs = soup.findAll('hr')
                for hr in hrs:
                    hr.extract()

        # Change <h1> to <h3> - used in editorial blogs
        masthead = soup.find("h1")
        if masthead:
            # Nuke the href
            if masthead.a:
                del(masthead.a['href'])
            tag = Tag(soup, "h3")
            tag.insert(0, self.fixChars(masthead.contents[0]))
            masthead.replaceWith(tag)

        # Change <span class="bold"> to <b>
        for subhead in soup.findAll(True, {'class':'bold'}) :
            if subhead.contents:
                bTag = Tag(soup, "b")
                bTag.insert(0, subhead.contents[0])
                subhead.replaceWith(bTag)

        divTag = soup.find('div',attrs={'id':'articleBody'})
        if divTag:
            divTag['class'] = divTag['id']

        # Add class="authorId" to <div> so we can format with CSS
        divTag = soup.find('div',attrs={'id':'authorId'})
        if divTag and divTag.contents[0]:
            tag = Tag(soup, "p")
            tag['class'] = "authorId"
            tag.insert(0, self.fixChars(self.tag_to_string(divTag.contents[0],
                             use_alt=False)))
            divTag.replaceWith(tag)

        return soup