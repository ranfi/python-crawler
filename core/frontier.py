import Queue
import time
from task import Task
import process
from worker import WorkerHandler  as worker

NUM_WORKERS = 1

class Frontier(object):
    
    '''
    Initialize a thread lock
    '''
    def __init__(self, job, db):
        self.job = job
        self.taskQueue = Queue.Queue(0)
        self.processs = []
        self.db = db
        doc = self.job.getDoc()
        rootEle = doc.getroot()
        self.nameSpace = rootEle.attrib["ns"]
        self.charSet = rootEle.attrib["charSet"]
        
        self.taskQueue.put(self.getTask(rootEle))
        '''
        Initialize process
        '''
        self.processs.append(process.UrlPreProcess())
        self.processs.append(process.CrawlerProcess())
        self.processs.append(process.NodeProcess())
        self.processs.append(process.ExtractProcess())
        self.processs.append(process.LoopProcess())
        self.processs.append(process.PaginateProcess())
        self.processs.append(process.ChildrenProcess())
        

    def getTaskSize(self):
        return self.taskQueue.qsize()
    
    def addTask(self, task):
        self.taskQueue.put(task,True, None)
     
    def getTask(self, rootEle):
        task = Task(self)
        task.setCrawlerEle(rootEle)
        return task

    def getNameSpace(self):
        return self.nameSpace
        
    def execute(self):
        try:
            #launch multithreading to execute
            for i in range(1, int(NUM_WORKERS)+1, 1):
                t = worker(self.taskQueue, self.processs, i)
                t.daemon = True
                t.start()

            self.taskQueue.join()

        except IOError, e:
            print "executing have an exception occurred"
        
