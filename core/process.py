# -*- encoding: utf-8 -*-

import urllib2
from abc import ABCMeta, abstractmethod
import sys
import datetime, time
import threading
from task import Task
from common import entity, datanode
from util import parseutil, log


reload(sys)
sys.setdefaultencoding('utf-8')

'''
 defined an abstract class for crawler execute process
'''

lock = threading.Lock()
logger = log.logging


class Process(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(task):
        pass

    def saveNode(self, db, node, parent_id):
        return db.execute_lastrowid(
            "insert into cr_node(name,value,level,url,parent_id,is_last,create_time) values(%s,%s,%s,%s,%s,%s,%s)",
            node.name, node.value, node.level, node.url,
            parent_id, node.is_last, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    def saveAttr(self, task, value):
        #获取数据库连接
        db = task.getFrontier().db

        ele = task.getCrawlerEle()
        attrName = ele.attrib[datanode.NAME]

        if lock.acquire():
            node = task.parentNode
            value = '' if value == None else value
            #node.name = attrName
            if node != None:
                nodeValue = node.value
                if nodeValue is not None and nodeValue != '':
                    nodeValue += datanode.SPLIT_NAME + attrName + datanode.SPLIT_VALUE + value
                else:
                    nodeValue = attrName + datanode.SPLIT_VALUE + value
                    #累加当前属性值到父节点
                task.parentNode.index = task.parentNode.index + 1
                node.value = nodeValue
                ## when isLast is equivalent to "true" to save
                if task.parentNode.is_last == 1:
                    self.saveNode(db, node, task.parentId)
        lock.release()


class UrlPreProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        #获取抓取URL
        try:
            crawlerUrl = task.nextCrawlerUrl
            if crawlerUrl == None or crawlerUrl == '':
                crawlerEle = task.crawlerEle

                if crawlerEle != None:
                    crawlerUrl = crawlerEle.attrib[datanode.URL] if crawlerEle.attrib.has_key(datanode.URL) else None

                urlXpath = crawlerEle.attrib[datanode.URL_XPATH] if crawlerEle.attrib.has_key(
                    datanode.URL_XPATH) else None
                urlRule = crawlerEle.attrib[datanode.URL_RULE] if crawlerEle.attrib.has_key(datanode.URL_RULE) else None

                if urlXpath != None and urlXpath != '':
                    crawlerUrl = parseutil.extractValueByXpath(urlXpath, task.frontier.getNameSpace(), task.htmlNode)

                    if urlRule != None and urlRule != '':
                        crawlerUrl = parseutil.extractValueByRule(urlRule, crawlerUrl)

                #如果xpath无法获取,则再次尝试正则处理
                #TODO

                #设定下一次抓取URL
                task.nextCrawlerUrl = crawlerUrl
        except Exception, e:
            print e
            print "execute UrlPreProcess has an exception"


class CrawlerProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):

        #获取抓取URL
        crawlerUrl = task.nextCrawlerUrl

        if crawlerUrl != None and crawlerUrl != '':
            self.startCrawler(task, crawlerUrl)


    def startCrawler(self, task, crawlerUrl):
        #获取数据库连接
        db = task.getFrontier().db
        query = "select id,url,content,status from cr_page where url = %s"
        data = db.get(query, crawlerUrl)
        if data != None:
            self.parseHtmlContent(task, data["content"])
        else:
            self.saveCrawlerPage(crawlerUrl, db, task)


    def parseHtmlContent(self, task, htmlContent):
        try:
            doc = parseutil.getFormatHtml(htmlContent)
        except Exception, e:
            msg = "get html content has an exception occurred"
            logger.error(msg)

        if task.htmlNode != None:
            task.lastNode = task.htmlNode

        task.htmlNode = doc


    def saveCrawlerPage(self, crawlerUrl, db, task):
        req = urllib2.Request(crawlerUrl)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Charset', 'utf-8;q=0.7,*;q=0.3')
        req.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
        req.add_header("Cookie", None)

        res = None
        try:
            res = urllib2.urlopen(req)
            page_html = res.read()

            ##保持抓取的内容
            query = "insert into cr_page(url,content,status) values(%s,%s,1)"
            id = db.execute(query, crawlerUrl, page_html.encode('utf-8'))
            self.parseHtmlContent(task, page_html)

        except urllib2.URLError, e:
            msg = "crawler a page has an exception" % crawlerUrl
            logger.error(msg)

        finally:
            if res != None:
                res.close()


class NodeProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        db = task.getFrontier().db
        tagName = task.crawlerEle.tag
        try:
            if tagName != '' and tagName == datanode.NODE:
                nodeName = task.getCrawlerEle().attrib[datanode.NAME]
                level = task.getCrawlerEle().attrib[datanode.LEVEL] if task.getCrawlerEle().attrib.has_key(
                    datanode.LEVEL) else 0
                node = entity.Node()
                node.level = level
                if task.parentId > 0:
                    node.parent_id = task.parentId
                node.name = nodeName
                if task.nextCrawlerUrl != '':
                    node.url = task.nextCrawlerUrl
                id = self.saveNode(db, node, task.parentId)
                node.id = id
                task.parentNode = node
                task.parentId = id

        except Exception, e:
            print e, "executing NodeProcess has occurred exception"


class ExtractProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        ele = task.crawlerEle
        tagName = task.crawlerEle.tag
        value = ''
        try:
            if tagName == datanode.ATTR:

                extractXpath = ele.attrib[datanode.EXTRACT_XPATH] if ele.attrib.has_key(
                    datanode.EXTRACT_XPATH) else None
                extractRule = ele.attrib[datanode.EXTRACT_RULE] if ele.attrib.has_key(datanode.EXTRACT_RULE) else None
                isLast = ele.attrib[datanode.IS_LAST] if ele.attrib.has_key(datanode.IS_LAST) else "false"
                name = ele.attrib[datanode.NAME] if ele.attrib.has_key(datanode.NAME) else None

                if extractXpath != None and extractXpath != '':
                    value = parseutil.extractValueByXpath(extractXpath, task.frontier.getNameSpace(), task.htmlNode)

                    extractRuleStr = ele.attrib[datanode.EXTRACT_RULE_STR] if ele.attrib.has_key(
                        datanode.EXTRACT_RULE_STR) else None
                    value = parseutil.extractValueByRule(extractRuleStr,
                                                         value) if extractRuleStr != None and extractRuleStr != '' else value
                else:
                    if extractRule != None and extractRule != '':
                        value = parseutil.extractValueByRule(extractRule, task.htmlNode.tostring())

                task.parentNode.is_last = (1 if isLast == 'true' else 0)

                self.saveAttr(task, value)

        except Exception, e:
            msg = "executing ExtractProcess has occurred exception, attrname is : %s" % name
            print e, msg
            logger.error(msg)


class LoopProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        ele = task.crawlerEle
        if ele.tag != datanode.LOOP:
            return
        try:
            loopXpath = ele.attrib[datanode.LOOP_XPATH] if ele.attrib.has_key(datanode.LOOP_XPATH) else None
            loopRule = ele.attrib[datanode.LOOP_RULE] if ele.attrib.has_key(datanode.LOOP_RULE) else None

            if loopXpath != None and loopXpath != '':
                if task.htmlNode != None:
                    loopEles = parseutil.selectNodes(loopXpath, task.frontier.getNameSpace(), task.htmlNode)

                    for loopEle in loopEles:
                        self.createChildren(task, loopEle)
        except Exception, e:
            print e, "executing LoopProcess has occurred exception"


    def createChildren(self, task, loopEle):
        ele = task.crawlerEle
        for child in list(ele):
            childTask = Task(task.getFrontier())
            childTask.setCrawlerEle(child)
            childTask.htmlNode = loopEle
            childTask.url = task.url
            #childTask.nextCrawlerUrl = task.nextCrawlerUrl
            childTask.parentId = task.parentId
            childTask.parentNode = task.parentNode
            childTask.getFrontier().addTask(childTask)


class PaginateProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        ele = task.crawlerEle
        paginateXpath = ele.attrib[datanode.PAGINATE_XPATH] if ele.attrib.has_key(datanode.PAGINATE_XPATH) else None
        if paginateXpath == None or task.hasPagiNate:
            return
        try:
            htmlNode = task.htmlNode
            if None != htmlNode:
                loopEles = parseutil.selectNodes(paginateXpath, task.frontier.getNameSpace(), htmlNode)
                paginateMaxXpath = ele.attrib[datanode.PAGINATE_MAX_XPATH] if ele.attrib.has_key(
                    datanode.PAGINATE_MAX_XPATH) else None
                paginateMaxRule = ele.attrib[datanode.PAGINATE_MAX_RULE] if ele.attrib.has_key(
                    datanode.PAGINATE_MAX_RULE) else None

                paginateUrlXpath = ele.attrib[datanode.PAGINATE_URL_XPATH] if ele.attrib.has_key(
                    datanode.PAGINATE_URL_XPATH) else None
                paginateUrlRule = ele.attrib[datanode.PAGINATE_URL_RULE] if ele.attrib.has_key(
                    datanode.PAGINATE_URL_RULE) else None

                maxPage = 0
                url = ''
                for child in loopEles:
                    if None != paginateMaxXpath and '' != paginateMaxXpath:
                        maxPage = parseutil.extractValueByXpath(paginateMaxXpath, task.frontier.getNameSpace(), child)
                        if None != paginateMaxRule and '' != paginateMaxRule:
                            maxPage = parseutil.extractValueByRule(paginateMaxRule, maxPage)
                    else:
                        maxPage = parseutil.extractValueByRule(paginateMaxRule, child.tostring())

                    if None != paginateUrlXpath and '' != paginateUrlXpath:
                        url = parseutil.extractValueByXpath(paginateUrlXpath, task.frontier.getNameSpace(), child)
                        if None != paginateUrlRule and '' != paginateUrlRule:
                            url = parseutil.extractValueByRule(paginateUrlRule, url)
                    else:
                        if None != paginateUrlRule and '' != paginateUrlRule:
                            url = parseutil.extractValueByRule(paginateUrlRule, child.tostring())

                if ('' != maxPage and int(maxPage) > 0) and url != '':

                    for i in range(2, int(maxPage) + 1, 1):
                        nextPageUrl = "http://place.qyer.com" + url + str(i)
                        childTask = Task(task.getFrontier())
                        childTask.setCrawlerEle(task.getCrawlerEle())
                        if task.htmlNode is not None:
                            childTask.htmlNode = task.htmlNode

                        childTask.nextCrawlerUrl = nextPageUrl
                        childTask.parentId = task.parentId
                        childTask.parentNode = task.parentNode
                        childTask.hasPagiNate = True
                        childTask.getFrontier().addTask(childTask)
        except Exception, e:
            print e, "executing PaginateProcess has occurred exception"


class ChildrenProcess(Process):
    def __init__(self):
        pass

    def execute(self, task):
        #如果是loop节点的话不处理子任务
        ele = task.crawlerEle
        try:
            if ele.tag != datanode.LOOP:
                self.createChildren(task)

        except Exception, e:
            print e, "executing ChildrenProcess has occurred exception"


    def createChildren(self, task):
        ele = task.crawlerEle
        count = len(list(ele))
        for child in list(ele):
            childTask = Task(task.getFrontier())
            childTask.childNum = count
            childTask.setCrawlerEle(child)
            childTask.htmlNode = task.htmlNode
            childTask.url = task.url
            childTask.parentId = task.parentId
            childTask.parentNode = task.parentNode
            childTask.getFrontier().addTask(childTask)
		





