#!/usr/bin/env python

import asyncio
import json
import sys
import websockets
from websockets.asyncio.server import serve

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
    return "NotImplemented"

#########################################################
# Handler for performing server tasks of one client connection
#########################################################
async def handler(websocket):
    pass

#########################################################
# Code for starting the server 
#########################################################
async def serverMain():          
    pass

# Called by the main module to start the server
def startServer(portToUse, storageToUse, serverID=0): 
    global port
    global storage
    global myID
    
    port = portToUse
    storage = storageToUse
    
    # ...
    