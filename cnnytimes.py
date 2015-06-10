#!/usr/bin/env  python
# -*- coding: utf-8 -*-
__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal <kovid at kovidgoyal.net>'
'''
cn.nytimes.com
'''
import re, string, time
from calibre import entity_to_unicode, strftime
from datetime import timedelta, date
from calibre.web.feeds.recipes import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup, Tag, BeautifulStoneSoup


class NYTimes(BasicNewsRecipe):

    # set headlinesOnly to True for the headlines-only version. If True, webEdition is ignored.
    headlinesOnly = False

    # set webEdition to True for the Web edition of the newspaper. Set oldest_article to the
    # number of days old an article can be for inclusion. If oldest_article = 0 all articles
    # will be included. Note: oldest_article is ignored if webEdition = False
    webEdition = False
    oldest_article = 7

    # replace paid Kindle Version:  the name will be changed to "The New York Times" to cause
    # previous paid versions of the new york times to best sent to the back issues folder on the kindle
    replaceKindleVersion = False

    # download higher resolution images than the small thumbnails typically included in the article
    # the down side of having large beautiful images is the file size is much larger, on the order of 7MB per paper
    useHighResImages = True

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
    one_picture_per_article = False

    # The maximum number of articles that will be downloaded
    max_articles_per_feed = 100

    # Whether to omit duplicates of articles (typically arsing when articles are indexed in
    # more than one section). If True, only the first occurance will be downloaded.
    filterDuplicates = True

    # Sections to collect for the Web edition.
    # Delete any you don't want, or use includeSections or excludeSections
    web_sections = [(u'����',u'world'),
                    (u'�й�',u'china'),
                    (u'��ҵ�뾭��','business'),
                    (u'�Ƽ�',u'science-technology'),
                    (u'�Ļ�',u'culture-arts'),
                    (u'����',u'life-fashion'),
                    (u'����',u'travel'),
                    (u'�����뽡��',u'education'),
                    (u'�۵�������',u'opinion')]

    if headlinesOnly:
        title='New York Times Headlines'
        description = 'Headlines from the New York Times'
        needs_subscription = True
    elif webEdition:
        title='New York Times (Web)'
        description = 'New York Times on the Web'
        needs_subscription = True
    elif replaceKindleVersion:
        title='The New York Times'
        description = 'Today\'s New York Times'
        needs_subscription = True
    else:
        title='New York Times'
        description = 'Today\'s New York Times. Needs subscription from http://cn.nytimes.com'
        needs_subscription = True


    month_list = ['january','february','march','april','may','june','july','august','september','october','november','december']

    def decode_us_date(self,datestr):
        udate = datestr.strip().lower().split()
        try:
            m = self.month_list.index(udate[0])+1
        except:
            return date.today()
        d = int(udate[1])
        y = int(udate[2])
        try:
            d = date(y,m,d)
        except:
            d = date.today
        return d

    earliest_date = date.today() - timedelta(days=oldest_article)

    __author__  = 'GRiker/Kovid Goyal/Nick Redding/Ben Collier'
    language = 'zh-cn'
    requires_version = (0, 7, 5)


    timefmt = ''
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
                            #'icon enlargeThis', #removed to provide option for high res images
                            'leftNavTabs',
                            'metaFootnote',
                            'module box nav',
                            'nextArticleLink',
                            'nextArticleLink clearfix',
                            'post-tools',
                            'relatedSearchesModule',
                            'side_tool',
                            'singleAd',
                            'entry entry-utility', #added for DealBook
                            'entry-tags', #added for DealBook
                            'footer promos clearfix', #added for DealBook
                            'footer links clearfix', #added for DealBook
                            'tabsContainer', #added for other blog downloads
                            'column lastColumn', #added for other blog downloads
                            'pageHeaderWithLabel', #added for other gadgetwise downloads
                            'column two', #added for other blog downloads
                            'column two last', #added for other blog downloads
                            'column three', #added for other blog downloads
                            'column three last', #added for other blog downloads
                            'column four',#added for other blog downloads
                            'column four last',#added for other blog downloads
                            'column last', #added for other blog downloads
                            'timestamp published', #added for other blog downloads
                            'entry entry-related',
                            'subNavigation tabContent active', #caucus blog navigation
                            'columnGroup doubleRule',
                            'mediaOverlay slideshow',
                            'headlinesOnly multiline flush',
                            'wideThumb',
                            'video', #added 02-11-2011
                            'videoHeader',#added 02-11-2011
                            'articleInlineVideoHolder', #added 02-11-2011
                            'assetCompanionAd',
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
                            'skybox', #added for DealBook
                            'TopAd', #added for DealBook
                            'related-content', #added for DealBook
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


    articles = {}
    key = None
    ans = []
    url_list = []

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

    def exclude_url(self,url):
        if not url.startswith("http"):
            return True
        if not url.endswith(".html") and 'dealbook.nytimes.com' not in url and 'blogs.nytimes.com' not in url: #added for DealBook
            return True
        if 'nytimes.com' not in url:
            return True
        if 'podcast' in url:
            return True
        if '/video/' in url:
            return True
        if '/slideshow/' in url:
            return True
        if '/magazine/index' in url:
            return True
        if '/interactive/' in url:
            return True
        if '/reference/' in url:
            return True
        if '/premium/' in url:
            return True
        return False

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
            br.form = br.forms().next()
            br['userid']   = self.username
            br['password'] = self.password
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
                br = self.clone_browser(self.browser)
                f = br.open_novisit(url_or_raw)
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

    def feed_title(self,div):
        return ''.join(div.findAll(text=True, recursive=True)).strip()

    def handle_article(self,div):
        thumbnail = div.find('div','thumbnail')
        if thumbnail:
            thumbnail.extract()
        a = div.find('a', href=True)
        if not a:
            return
        url = re.sub(r'\?.*', '', a['href'])
        if self.exclude_url(url):
            return
        url += '?pagewanted=all'
        if self.filterDuplicates:
            if url in self.url_list:
                return
        self.url_list.append(url)
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
        feed = self.key if self.key is not None else 'Uncategorized'
        if not self.articles.has_key(feed):
            self.ans.append(feed)
            self.articles[feed] = []
        self.articles[feed].append(
                        dict(title=title, url=url, date=pubdate,
                            description=description, author=author,
                            content=''))


    def parse_web_edition(self):

        for (sec_title,index_url) in self.web_sections:
            if self.includeSections != []:
                if sec_title not in self.includeSections:
                    print "SECTION NOT INCLUDED: ",sec_title
                    continue
            if sec_title in self.excludeSections:
                print "SECTION EXCLUDED: ",sec_title
                continue
            print 'Index URL: '+'http://www.nytimes.com/pages/'+index_url+'/index.html'
            soup = self.index_to_soup('http://www.nytimes.com/pages/'+index_url+'/index.html')
            self.key = sec_title
            # Find each article
            for div in soup.findAll(True,
                attrs={'class':['section-headline', 'story', 'story headline','sectionHeader','headlinesOnly multiline flush']}):
                if div['class'] in ['story', 'story headline'] :
                    self.handle_article(div)
                elif div['class'] == 'headlinesOnly multiline flush':
                    for lidiv in div.findAll('li'):
                        self.handle_article(lidiv)

        self.ans = [(k, self.articles[k]) for k in self.ans if self.articles.has_key(k)]
        return self.filter_ans(self.ans)


    def parse_todays_index(self):

        soup = self.index_to_soup('http://www.nytimes.com/pages/todayspaper/index.html')

        skipping = False
        # Find each article
        for div in soup.findAll(True,
            attrs={'class':['section-headline', 'story', 'story headline','sectionHeader','headlinesOnly multiline flush']}):

            if div['class'] in ['section-headline','sectionHeader']:
                self.key = string.capwords(self.feed_title(div))
                self.key = self.key.replace('Op-ed','Op-Ed')
                self.key = self.key.replace('U.s.','U.S.')
                self.key = self.key.replace('N.y.','N.Y.')
                skipping = False
                if self.includeSections != []:
                    if self.key not in self.includeSections:
                        print "SECTION NOT INCLUDED: ",self.key
                        skipping = True
                if self.key in self.excludeSections:
                    print "SECTION EXCLUDED: ",self.key
                    skipping = True

            elif div['class'] in ['story', 'story headline'] :
                if not skipping:
                    self.handle_article(div)
            elif div['class'] == 'headlinesOnly multiline flush':
                for lidiv in div.findAll('li'):
                    if not skipping:
                        self.handle_article(lidiv)

        self.ans = [(k, self.articles[k]) for k in self.ans if self.articles.has_key(k)]
        return self.filter_ans(self.ans)

    def parse_headline_index(self):

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
                    if self.includeSections != []:
                        if section_name not in self.includeSections:
                            print "SECTION NOT INCLUDED: ",section_name
                            continue
                    if section_name in self.excludeSections:
                        print "SECTION EXCLUDED: ",section_name
                        continue

                    section_name=string.capwords(section_name)
                    section_name = section_name.replace('Op-ed','Op-Ed')
                    section_name = section_name.replace('U.s.','U.S.')
                    section_name = section_name.replace('N.y.','N.Y.')
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
                        if self.exclude_url(url):
                            continue
                        url += '?pagewanted=all'
                        if self.filterDuplicates:
                            if url in self.url_list:
                                continue
                        self.url_list.append(url)
                        title = self.tag_to_string(a, use_alt=True).strip()
                        desc = h3_item.find('p')
                        if desc is not None:
                            description = self.tag_to_string(desc,use_alt=False)
                        else:
                            description = ''
                        if not self.articles.has_key(section_name):
                            self.ans.append(section_name)
                            self.articles[section_name] = []
                        self.articles[section_name].append(dict(title=title, url=url, date=pubdate, description=description, author=author, content=''))

        self.ans = [(k, self.articles[k]) for k in self.ans if self.articles.has_key(k)]
        return self.filter_ans(self.ans)

    def parse_index(self):
        if self.headlinesOnly:
            return self.parse_headline_index()
        elif self.webEdition:
            return self.parse_web_edition()
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
        if self.webEdition & (self.oldest_article>0):
            date_tag = soup.find(True,attrs={'class': ['dateline','date']})
            if date_tag:
                date_str = self.tag_to_string(date_tag,use_alt=False)
                date_str = date_str.replace('Published:','')
                date_items = date_str.split(',')
                try:
                    datestring = date_items[0]+' '+date_items[1]
                    article_date = self.decode_us_date(datestring)
                except:
                    article_date = date.today()
                if article_date < self.earliest_date:
                    self.log("Skipping article dated %s" % date_str)
                    return None

        #all articles are from today, no need to print the date on every page
        try:
            if not self.webEdition:
                date_tag = soup.find(True,attrs={'class': ['dateline','date']})
                if date_tag:
                    date_tag.extract()
        except:
            self.log("Error removing the published date")

        if self.useHighResImages:
            try:
                #open up all the "Enlarge this Image" pop-ups and download the full resolution jpegs
                enlargeThisList = soup.findAll('div',{'class':'icon enlargeThis'})
                if enlargeThisList:
                    for popupref in enlargeThisList:
                        popupreflink = popupref.find('a')
                        if popupreflink:
                            reflinkstring = str(popupreflink['href'])
                            refstart = reflinkstring.find("javascript:pop_me_up2('") + len("javascript:pop_me_up2('")
                            refend = reflinkstring.find(".html", refstart) + len(".html")
                            reflinkstring = reflinkstring[refstart:refend]

                            popuppage = self.browser.open(reflinkstring)
                            popuphtml = popuppage.read()
                            popuppage.close()
                            if popuphtml:
                                st = time.localtime()
                                year = str(st.tm_year)
                                month = "%.2d" % st.tm_mon
                                day = "%.2d" % st.tm_mday
                                imgstartpos = popuphtml.find('http://graphics8.nytimes.com/images/' + year + '/' +  month +'/' + day +'/') + len('http://graphics8.nytimes.com/images/' + year + '/' +  month +'/' + day +'/')
                                highResImageLink = 'http://graphics8.nytimes.com/images/' + year + '/' +  month +'/' + day +'/' + popuphtml[imgstartpos:popuphtml.find('.jpg',imgstartpos)+4]
                                popupSoup = BeautifulSoup(popuphtml)
                                highResTag = popupSoup.find('img', {'src':highResImageLink})
                                if highResTag:
                                    try:
                                        newWidth = highResTag['width']
                                        newHeight = highResTag['height']
                                        imageTag = popupref.parent.find("img")
                                    except:
                                        self.log("Error: finding width and height of img")
                                    popupref.extract()
                                    if imageTag:
                                        try:
                                            imageTag['src'] = highResImageLink
                                            imageTag['width'] = newWidth
                                            imageTag['height'] = newHeight
                                        except:
                                            self.log("Error setting the src width and height parameters")
            except Exception:
                self.log("Error pulling high resolution images")

            try:
                #remove "Related content" bar
                runAroundsFound = soup.findAll('div',{'class':['articleInline runaroundLeft','articleInline doubleRule runaroundLeft','articleInline runaroundLeft firstArticleInline','articleInline runaroundLeft  ','articleInline runaroundLeft  lastArticleInline']})
                if runAroundsFound:
                    for runAround in runAroundsFound:
                        #find all section headers
                        hlines = runAround.findAll(True ,{'class':['sectionHeader','sectionHeader flushBottom']})
                        if hlines:
                            for hline in hlines:
                                hline.extract()

                        #find all section headers
                        hlines = runAround.findAll('h6')
                        if hlines:
                            for hline in hlines:
                                hline.extract()
            except:
                self.log("Error removing related content bar")


            try:
                #in case pulling images failed, delete the enlarge this text
                enlargeThisList = soup.findAll('div',{'class':'icon enlargeThis'})
                if enlargeThisList:
                    for popupref in enlargeThisList:
                        popupref.extract()
            except:
                self.log("Error removing Enlarge this text")

        return self.strip_anchors(soup)

    def postprocess_html(self,soup, True):
        try:
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
        except:
                self.log("ERROR: One picture per article in postprocess_html")

        try:
                # Change captions to italic
                for caption in soup.findAll(True, {'class':'caption'}) :
                        if caption and len(caption) > 0:
                                cTag = Tag(soup, "p", [("class", "caption")])
                                c = self.fixChars(self.tag_to_string(caption,use_alt=False)).strip()
                                mp_off = c.find("More Photos")
                                if mp_off >= 0:
                                        c = c[:mp_off]
                                cTag.insert(0, c)
                                caption.replaceWith(cTag)
        except:
                self.log("ERROR:  Problem in change captions to italic")

        try:
                # Change <nyt_headline> to <h2>
                h1 = soup.find('h1')
                blogheadline = str(h1) #added for dealbook
                if h1:
                        headline = h1.find("nyt_headline")
                        if headline:
                                tag = Tag(soup, "h2")
                                tag['class'] = "headline"
                                tag.insert(0, self.fixChars(headline.contents[0]))
                                h1.replaceWith(tag)
                        elif blogheadline.find('entry-title'):#added for dealbook
                                tag = Tag(soup, "h2")#added for dealbook
                                tag['class'] = "headline"#added for dealbook
                                tag.insert(0, self.fixChars(h1.contents[0]))#added for dealbook
                                h1.replaceWith(tag)#added for dealbook

                else:
                        # Blog entry - replace headline, remove <hr> tags  - BCC I think this is no longer functional 1-18-2011
                        headline = soup.find('title')
                        if headline:
                                tag = Tag(soup, "h2")
                                tag['class'] = "headline"
                                tag.insert(0, self.fixChars(headline.renderContents()))
                                soup.insert(0, tag)
                                hrs = soup.findAll('hr')
                                for hr in hrs:
                                        hr.extract()
        except:
                self.log("ERROR:  Problem in Change <nyt_headline> to <h2>")

        try:
                #if this is from a blog (dealbook, fix the byline format
                bylineauthor = soup.find('address',attrs={'class':'byline author vcard'})
                if bylineauthor:
                    tag = Tag(soup, "h6")
                    tag['class'] = "byline"
                    tag.insert(0, self.fixChars(bylineauthor.renderContents()))
                    bylineauthor.replaceWith(tag)
        except:
            self.log("ERROR:  fixing byline author format")

        try:
                #if this is a blog (dealbook) fix the credit style for the pictures
                blogcredit = soup.find('div',attrs={'class':'credit'})
                if blogcredit:
                    tag = Tag(soup, "h6")
                    tag['class'] = "credit"
                    tag.insert(0, self.fixChars(blogcredit.renderContents()))
                    blogcredit.replaceWith(tag)
        except:
            self.log("ERROR:  fixing credit format")


        try:
                # Change <h1> to <h3> - used in editorial blogs
                masthead = soup.find("h1")
                if masthead:
                        # Nuke the href
                        if masthead.a:
                                del(masthead.a['href'])
                        tag = Tag(soup, "h3")
                        tag.insert(0, self.fixChars(masthead.contents[0]))
                        masthead.replaceWith(tag)
        except:
                self.log("ERROR:  Problem in Change <h1> to <h3> - used in editorial blogs")

        try:
                # Change <span class="bold"> to <b>
                for subhead in soup.findAll(True, {'class':'bold'}) :
                        if subhead.contents:
                                bTag = Tag(soup, "b")
                                bTag.insert(0, subhead.contents[0])
                                subhead.replaceWith(bTag)
        except:
                self.log("ERROR:  Problem in Change <h1> to <h3> - used in editorial blogs")
        try:
                #remove the <strong> update tag
                blogupdated = soup.find('span', {'class':'update'})
                if blogupdated:
                    blogupdated.replaceWith("")
        except:
                self.log("ERROR:  Removing strong tag")

        try:
                divTag = soup.find('div',attrs={'id':'articleBody'})
                if divTag:
                        divTag['class'] = divTag['id']
        except:
                self.log("ERROR:  Problem in soup.find(div,attrs={id:articleBody})")

        try:
                # Add class="authorId" to <div> so we can format with CSS
                divTag = soup.find('div',attrs={'id':'authorId'})
                if divTag and divTag.contents[0]:
                        tag = Tag(soup, "p")
                        tag['class'] = "authorId"
                        tag.insert(0, self.fixChars(self.tag_to_string(divTag.contents[0],
                                                         use_alt=False)))
                        divTag.replaceWith(tag)
        except:
                self.log("ERROR:  Problem in Add class=authorId to <div> so we can format with CSS")

        return soup
    def populate_article_metadata(self, article, soup, first):
        if first and hasattr(self, 'add_toc_thumbnail'):
            idxdiv = soup.find('div',attrs={'class':'articleSpanImage'})
            if idxdiv is not None:
                if idxdiv.img:
                    self.add_toc_thumbnail(article, idxdiv.img['src'])
            else:
                img = soup.find('img')
                if img is not None:
                    self.add_toc_thumbnail(article, img['src'])

        shortparagraph = ""
        try:
            if len(article.text_summary.strip()) == 0:
                articlebodies = soup.findAll('div',attrs={'class':'articleBody'})
                if not articlebodies: #added to account for blog formats
                    articlebodies = soup.findAll('div', attrs={'class':'entry-content'}) #added to account for blog formats
                if articlebodies:
                    for articlebody in articlebodies:
                        if articlebody:
                            paras = articlebody.findAll('p')
                            for p in paras:
                                refparagraph = self.massageNCXText(self.tag_to_string(p,use_alt=False)).strip()
                                #account for blank paragraphs and short paragraphs by appending them to longer ones
                                if len(refparagraph) > 0:
                                    if len(refparagraph) > 140: #approximately two lines of text
                                        article.summary = article.text_summary = shortparagraph + refparagraph
                                        return
                                    else:
                                        shortparagraph = refparagraph + " "
                                        if shortparagraph.strip().find(" ") == -1 and not shortparagraph.strip().endswith(":"):
                                            shortparagraph = shortparagraph + "- "

        except:
            self.log("Error creating article descriptions")
            return

\