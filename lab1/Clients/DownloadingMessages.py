import BoardProxy
import os
import sys
import threading 
import time

serverPorts = [10000]

serverProxies = [BoardProxy.storage(port) for port in serverPorts] # Create Proxies for each server.

def downloadFromServer():

    s = serverProxies[0]
    startTime = time.time()
    for i in range(s.getNum()):
        s.get(i)
    endTime = time.time()
    print(f"time to get every number individually {endTime-startTime}")

    time.sleep(1) # wait for severs to synchronize

    startTime = time.time()
    s.getBoard()
    endTime = time.time()
    print(f"time to get all messages at once {endTime-startTime}")



if __name__ == "__main__":
    downloadFromServer()

    for proxy in serverProxies:
        board = proxy.close()
