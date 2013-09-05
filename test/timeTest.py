import time,datetime



if __name__ == "__main__":
    startTime = time.time()
    time.sleep(1)
    endTime = time.time()
    print "Total run time %s seconds" % int((endTime-startTime)/1000*1000)