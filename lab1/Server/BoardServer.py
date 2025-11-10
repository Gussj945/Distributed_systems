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
    command = request.get("Operation", "").lower()

    match command:
        case "put":
            message = request["Message"]
            senderID = request.get("MYID", -1)
            result = await storage.put(message, senderID)
            return "Done"
        case "get":
            try:
                index = request["Index"]
                senderID = request.get("MYID", -1)
                result = await storage.get(index, senderID)
                return result
            except IndexError:
                return "UNKNOWN_INDEX" #CLIENT DOESNT DETECT ERROR AND PRINTSS MESSAGE 0: NONE INSTEAD WHAT TO DO?
        case "getnum":
            senderID = request.get("MYID", -1)
            result = await storage.getNum(senderID)
            return result
        case "getboard":
            senderID = request.get("MYID", -1)
            result = await storage.getBoard(senderID)
            return result
        case "modify":
            try: 
                senderID = request.get("MYID", -1)
                index = request["Index"]
                message = request["Message"]
                result = await storage.modify(index, message, senderID)
                return "DONE" #not displayed
            except IndexError:
                return "UNKNOWN_INDEX"
        case "delete":
            senderID = request.get("MYID", -1)
            index = request["Index"]
            await storage.delete(index, senderID)
            return "DONE"
        case "deleteall":
            senderID = request.get("MYID", -1)
            await storage.deleteAll(senderID)
            return "Done"
        case "close":
            return "OK"
        case _:
            return f"Unknown Command {request}"


#########################################################
# Handler for performing server tasks of one client connection
#########################################################
async def handler(websocket):
    try:
        async for message in websocket:
            request = json.loads(message)

            if request == "close":
                await websocket.send(json.dumps("Connection closed"))
                await websocket.close() 
                #await websocket.server.close()
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
def startServer(portToUse, storageToUse, serverID=0): 
    global port
    global storage
    global myID
    
    port = portToUse
    storage = storageToUse

    asyncio.run(serverMain())
  
    