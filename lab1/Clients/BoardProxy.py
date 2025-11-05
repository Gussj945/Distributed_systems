# Information on the websocket-client is available at 
# https://websocket-client.readthedocs.io/en/latest/

import logging
import websocket
import asyncio
import json

logging.basicConfig(
format= "%(asctime)s %(message)s",
level=logging.DEBUG,
)

class storage: 
    def __init__(self, port): 
        self.port = port
        self.url = f"ws://localhost:{self.port}"
        self.ws = None
        self.connected = False

    def connect(self):
        if self.connected == False:
            self.ws = websocket.create_connection(self.url)
            self.connected = True
       
    def doOperation(self, request): 
        try: 
            if self.connected != True:
                self.connect()
            
            self.ws.send(json.dumps(request))

            response_string = self.ws.recv()

            return json.loads(response_string)
            
        
        except Exception as e: 
            print(f"Error during doOperation: {e}")
    def put(self, message): 
        request = {"Operation": "put", "Message": message}
        return self.doOperation(request)

       
    def get(self, index): 
        request = {"Operation": "get", "Index": index}
        return self.doOperation(request)

    def getNum(self): 
        request = {"Operation": "getNum"}
        return self.doOperation(request)
        
    def getBoard(self): 
        request = {"Operation": "getBoard"}
        return self.doOperation(request)
        
    def modify(self, index, message): 
        request = {"Operation": "modify", "Index": index, "Message": message}
        return self.doOperation(request)
        
    def delete(self, index): 
        request = {"Operation": "delete", "Index": index}
        return self.doOperation(request)

    def deleteAll(self): 
        request = {"Operation": "deleteAll"}
        return self.doOperation(request)
        
    def close(self): 
        request = {"Operation": "deleteAll"}
        return self.doOperation(request)
        
        