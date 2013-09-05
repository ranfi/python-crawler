'''
 defined all of entity objects
'''


class Job(object):
    def __init__(self, jobName=None, status=None, dbConfig=None):
        self.jobName = ''
        self.status = 'N'
        self.dbConfig = dbConfig


class DBConfig(object):
    def __init__(self, host, dbName=None, userName=None, password=None, port=None, dialect=None):
        self.host = host
        self.dbName = dbName
        self.userName = userName
        self.password = password
        self.port = port if port is not None else 3306
        self.dialect = dialect if dialect is not None else 'mysql'


class Task(object):
    def __init__(self):
        self.task_id = -1
        self.task_name = ''
        self.task_status = 1
        self.start_time = None
        self.end_time = None
        self.page_id = -1


class Page(object):
    def __init__(self):
        self.id = 0
        self.url = ''
        self.content = None
        self.status = -1


class Node(object):
    def __init__(self):
        self.id = 0
        self.index = 0
        self.name = ''
        self.value = ''
        self.level = 0
        self.url = ''
        self.parent_id = 0
        self.is_last = 0
		
		
		
