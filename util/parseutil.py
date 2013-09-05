# -*- encoding: utf-8 -*-

import lxml.html.soupparser as soupparser
import xml.etree.ElementTree as ET
from lxml.html.clean import Cleaner
import logging
import os
import re


def readXml(file):
    return ET.parse(file)


def getAttributeValue(node, key):
    return node.attrib[key]


def getChildNode(node):
    for child in node:
        print child.tag, child.attrib


def getFormatHtml(htmlContent):
    try:
        dom = soupparser.fromstring(htmlContent)
    except Exception, e:
        cleaner = Cleaner()
        htmlContent = cleaner.clean_html(htmlContent)
        doc = soupparser.fromstring(htmlContent)

    return dom


def selectNodes(xpath, nameSpace, ele):
    nodes = ele.xpath(xpath, nameSpace)


"""
 根据xpath语法抽取节点的包含内容
"""


def extractValueByXpath(xpath, nameSpace, ele):
    nodes = ele.xpath(xpath, nameSpace=None)
    result = ''
    for node in nodes:
        result = node.text if ET.iselement(node) else node
        break;

    return result


def selectNodes(xpath, nameSpace, ele):
    return ele.xpath(xpath, nameSpace=None)


"""
 根据xpath语法和相应的属性名称抽取节点的属性值
"""


def extractAttrByXpath(xpath, nameSpace, ele, tagAttr):
    nodes = ele.xpath(xpath, nameSpace=None)
    result = []
    for node in nodes:
        if ET.iselement(node):
            result.append(node.attrib[tagAttr])
    return result[0] if len(result) == 1 else result


def extractValueByRule(rule, content):
    pattern = re.compile(rule)
    match = pattern.match(content.decode('utf8'))
    if match:
        return match.group(1)
    return ""


if __name__ == '__main__':
    doc = readXml("../conf/job.xml")
    nodes = doc.getiterator("job")
    for node in nodes:
        print node.attrib['name']
        db = node.find("db")
        print db.attrib['host']

    str = "...2:"
    regex = "[\D]*(\d+)[\D]*"
    value = extractValueByRule(regex, str)
    print "execute result is %s " % value





   