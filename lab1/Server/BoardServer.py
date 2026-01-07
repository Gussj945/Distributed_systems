#!/usr/bin/env python

import asyncio
import json
from websockets.asyncio.server import serve
import logging

logging.basicConfig(
    format= "%(asctime)s %(message)s",
    level=logging.DEBUG,
) 

# Storage in which the messages of the message board are stored.
storage = None


# Port number on which the server has to be started. 
port = -1 # Changed in function startServer


#########################################################
# Stub calling the methods on one storage object 
# depending on the type of message received.  
#########################################################
async def stub(request):
    """
    Stub: When it receives a request it calls the 
    corresponding method in the storage.
    
    Parameter request: Request message that is already parsed. 
                       It is a dictionary mapping the name of a field into its value. 
                       Example: {"COMMAND": "PUT", "MESSAGE": "How are you?"}
    Returns the response message. It is not yet encoded as JSON message.  
    """
    print(f"server stub got request{request}")
    command = request.get("Operation", "").lower()

    senderID = request.get("MYID", -1)
    if logicalClock:
        timeStamp = request.get("TimeStamp", None)
        if timeStamp != None: 
    # update logical clock (receive event)
            logicalClock.updateTime(timeStamp)

    response = {}

    match command:
        case "setcoordinator":
            if serverLeader: #TODO: Correct?                
                newCoordinatorID = request["newCoordinatorID"]
                #return await serverLeader.setCoordinator(newCoordinatorID)
                await serverLeader.setCoordinator(newCoordinatorID)
                response["Result"] = "OK"
            else:
                response["Result"] = "ERROR"
        case "election":
            if serverLeader:
                await serverLeader.election()
                response["Result"] = "OK"
            else:
                response["Result"] = "Error"
        case "areyoualive":
            response["Result"] = "YES"
        case "acquire":     #TODO should I add Id to mutex?
            if serverMutex == None:
                response["Result"] = "Error"
            #return await serverMutex.acquire()
            mutex = await serverMutex.acquire()
            response["Result"] = mutex
        case "release":
            if serverMutex == None:
                response["Result"] = "Error"
            result = await serverMutex.release()
            response["Result"] = result
        case "put":
            message = request["Message"]
            result = await storage.put(message, senderID)
            response["Result"] = "DONE"
        case "get":
            try:
                index = request["Index"]
                 #should just be done once for every command
                result = await storage.get(index, senderID)
                response["Result"] = result
            except IndexError:
                response["Result"] = "UNKNOWN INDEX"
        case "getnum":
            result = await storage.getNum(senderID)
            response["Result"] = result
        case "getboard":
            result = await storage.getBoard(senderID) #result dict [TimeStamp: latestTimeStamp, board]
            response["Result"] = result
        case "modify":
            try:                
                index = request["Index"]
                message = request["Message"]
                result = await storage.modify(index, message, senderID)
                response["Result"] = "DONE"
            except IndexError:
                response["Result"] = "UNKNOWN INDEX"
        case "delete":
            
            index = request["Index"]
            await storage.delete(index, senderID)
            response["Result"] = "DONE"
        case "deleteall":
            await storage.deleteAll(senderID)
            response["Result"] = "DONE"
        case "close":
            response["Result"] = "DONE"
        case _:
            return f"Unknown Command {request}"
        
    # Outgoing timestamp (send event)
    if logicalClock:
        response["TimeStamp"] = logicalClock.getTime()

    return response



#########################################################
# Handler for performing server tasks of one client connection
#########################################################
async def handler(websocket):
    try:
        async for message in websocket:
            request = json.loads(message)

            if request.get("Operation") == "close":
                try: 
                    await websocket.send(json.dumps("Connection closed"))
                    # give client a moment to receive connection closed msg
                    await asyncio.sleep(0.1)
                except Exception:
                    pass
                await websocket.close() 
                break
            else:
                response = await stub(request)

                await websocket.send(json.dumps(response))
        
    except Exception as e:
        print(f"Error occoured in handler: {e}")



#########################################################
# Code for starting the server 
#########################################################
async def serverMain():  
    async with serve(handler,"localhost", port) as server:
        await server.serve_forever()  
    

# Called by the main module to start the server
def startServer(portToUse, storageToUse, serverID=0, mutex=None, leaderElection=None, logicalClockParam=None): 
    global port
    global storage
    global myID
    global serverMutex
    global serverLeader
    global logicalClock
    
    myID = serverID #Forgot to implement this does it cause problems?
    port = portToUse
    storage = storageToUse
    serverMutex = mutex #correct?
    serverLeader = leaderElection
    logicalClock = logicalClockParam
    asyncio.run(serverMain())
  
    