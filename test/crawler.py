import urllib2
import lxml.html.soupparser as soupparser
import sys,json,time,string
import os
import logging


class CrawlerHandler(object):

    def __init__(self, url, cookie):
        print "init..."
        self.req = urllib2.Request(url)
        self.req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17')
        self.req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        self.req.add_header('Accept-Charset', 'utf-8;q=0.7,*;q=0.3')
        self.req.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
        self.req.add_header("Cookie", cookie)

    def getHtmlContent(self):
        page_html = ""
        try:
            res = urllib2.urlopen(self.req)
            page_html = res.read()
        except urllib2.URLError, e:
            print e, "urllib2.URLError"
            logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG)
            logging.shutdown()
        finally:
            res.close()
        return page_html

    def getElementNodesByXpath(self, page, xpath):
        try:
            htmlContent = soupparser.fromstring(page)
        except Exception:
            return -1
        return htmlContent.xpath(xpath)


if __name__ == "__main__":
    url = "http://place.qyer.com/country/"
    crawlerHandler = CrawlerHandler(url, "")
    page = crawlerHandler.getHtmlContent()
    val = crawlerHandler.getElementNodesByXpath(page,'//*[starts-with(@id,"continent")]/div/h2/a')
    for entry in val:
        print entry.text_content()




