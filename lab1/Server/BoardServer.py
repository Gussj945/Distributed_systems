#!/usr/bin/env python

import asyncio
import json
from websockets.asyncio.server import serve
import logging

""" logging.basicConfig(
    format= "%(asctime)s %(message)s",
    level=logging.DEBUG,
) """

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
            result = await storage.put(message)
            return "Done"
        case "get":
            try:
                index = request["Index"]
                result = await storage.get(index)
                return result
            except IndexError:
                return "UNKNOWN_INDEX" #CLIENT DOESNT DETECT ERROR AND PRINTSS MESSAGE 0: NONE INSTEAD WHAT TO DO?
        case "getnum":
            result = await storage.getNum()
            return result
        case "getboard":
            result = await storage.getBoard()
            return result
        case "modify":
            try: 
                index = request["Index"]
                message = request["Message"]
                result = await storage.modify(index, message)
                return "DONE" #not displayed
            except IndexError:
                return "UNKNOWN_INDEX"
        case "delete":
            index = request["Index"]
            await storage.delete(index)
            return "DONE"
        case "deleteall":
            await storage.deleteAll()
            return "Done"
        case "close":
            await storage.close()
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
  
    