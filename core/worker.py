import threading, sys
import time
from common import constant


lock = threading.Lock()


class WorkerHandler(threading.Thread):
    def __init__(self, taskQueue, processs, id):
        threading.Thread.__init__(self)
        self.taskQueue = taskQueue
        self.processs = processs
        self.badProcesss = list()
        self.id = id

    def run(self):
        startTime = time.time()
        while 1:
            task = None
            try:
                if lock.acquire():
                    size = self.taskQueue.qsize()
                    if size > 0:
                        print "The current size of taskQueue is: %s" % size
                        self.assignThreads(constant.MAX_PROCESS_THREADS_NUMBER)
                    else:
                        time.sleep(30)
                lock.release()

            except Exception, e:
                print e
                self.badProcesss.append(task)
                sys.exit(0)

        endTime = time.time()
        print "Total spend time %s seconds" % int((endTime - startTime) / 1000 * 1000)


    def assignThreads(self, num):
        for i in range(1, int(num) + 1, 1):
            if self.taskQueue.qsize() > 0:
                task = self.taskQueue.get()
                t = DispatchHandler(self.taskQueue, self.processs, task)
                t.start()
                t.join()
            else:
                break


class DispatchHandler(threading.Thread):
    def __init__(self, taskQueue, processs, task):
        threading.Thread.__init__(self)
        self.taskQueue = taskQueue
        self.task = task
        self.processs = processs

    def run(self):
        if self.task is not None:
            for process in self.processs:
                process.execute(self.task)


        


        
        
