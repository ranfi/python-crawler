# -*- encoding: utf-8 -*-
import xml.etree.ElementTree as ET
import torndb
from core import frontier, globalconfig
import sys


class LaunchJob(object):
    def __init__(self, job):
        self.job = job
        self.db = torndb.Connection(job.dbConfig.host, job.dbConfig.dbName, job.dbConfig.userName,
                                    job.dbConfig.password)
        self.doc = None
        self.frontier = None

    def getDoc(self):
        return self.doc

    def start(self):
        self.doc = ET.parse("xpath/" + self.job.jobName + ".xml")
        self.frontier = frontier.Frontier(self, self.db)
        self.frontier.execute()


if __name__ == "__main__":
    jobs = globalconfig.LoadConfig.parse()
    for job in jobs:
        print "Launch job : %s\n" % job.jobName
        status = job.status
        if status == 'Y':
            LaunchJob(job).start()