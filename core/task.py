class Task(object):
    
    def __init__(self, frontier):
        self.index = 0
        self.childNum = 0
        self.crawlerEle = None
        self.htmlNode = None
        self.htmlContent = ''
        self.frontier = frontier
        self.lastNode = None
        self.lastContent = ''
        self.url = ''
        self.nextCrawlerUrl = ''
        self.hasPagiNate = 0
        self.parentNode = None
        self.parentId = 0
        
    def setCrawlerEle(self, crawlerEle):
        self.crawlerEle = crawlerEle

    def getCrawlerEle(self):
        return self.crawlerEle


    def getFrontier(self):
        return self.frontier