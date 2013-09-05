__author__ = 'ranfi'

from util import parseutil
from common import entity


class LoadConfig:
    @staticmethod
    def parse(path=None):
        jobs = list()
        path = "conf/job.xml"
        doc = parseutil.readXml(path)
        nodes = doc.getiterator("job")
        for node in nodes:
            jobName = node.attrib['name']
            status = node.attrib['status']

            db = node.find("db")
            host = db.attrib['host']
            dbName = db.attrib['dbName']
            userName = db.attrib['userName']
            password = db.attrib['password']
            port = db.attrib['port']

            dbConfig = entity.DBConfig(host, dbName, userName, password, port, None)
            job = entity.Job()
            job.jobName = jobName
            job.status = status
            job.dbConfig = dbConfig
            jobs.append(job)
        return jobs




