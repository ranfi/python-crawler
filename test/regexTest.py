# -*- encoding: utf-8 -*-
from util import parseutil
import re







if __name__ == "__main__":
    str  = "http://maps.google.com/maps/api/staticmap?size=270x180&markers=icon:http://static.qyer.com/images/place/icon_coord_current.png|-80.417343,77.116013&sensor=false"
    regex = "[\w:\/\.\?x=&_]+\|([\-0-9,\.]+)&.*"
    value = parseutil.extractValueByRule(regex,str)
    print "execute result is %s " % value

    str = "啊rrrrr33中国"
    regex = "[\D]+(\d+).*"
    value = parseutil.extractValueByRule(regex,str)
    print "execute result is %s " % value

    str = "...38:"
    regex = "[\D]+(\d+)[\D]*"
    value = parseutil.extractValueByRule(regex,str)
    print "execute result is %s " % value

