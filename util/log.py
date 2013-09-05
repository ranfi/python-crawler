#!/usr/bin/python
# coding:UTF-8

import logging,os,time

now = time.strftime('%Y-%m-%d-%H',time.localtime(time.time()))
param = {
'filename' : os.path.join(os.getcwd() ,'log',now+'.txt'),
'level' : logging.INFO,
'filemode' : 'a',
'format' : '%(asctime)s - %(levelname)s: %(message)s',
}

logging.basicConfig(**param)


