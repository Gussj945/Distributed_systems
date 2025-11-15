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
        self.retry = 3

    def connect(self):
        if self.connected == False:
            self.ws = websocket.create_connection(self.url)
            self.connected = True
       
    def doOperation(self, request): 
        try: 
            if self.connected == False and request["Operation"] == "close":
                 return "Server is closed"
            elif self.connected == False:
                self.connect()
            
            self.ws.send(json.dumps(request))

            response_string = self.ws.recv()
            self.retry = 3
            print(f"returned {response_string}")

            return json.loads(response_string)
        #websocket.WebSocketConnectionClosedException, ConnectionResetError
        except (websocket.WebSocketConnectionClosedException, ConnectionResetError, ConnectionAbortedError) as e:
            print(f"connection lost: {e}. Reconnecting...")

            if self.retry > 0: 
                self.connected = False
                self.connect()
                self.retry -= 1
                return self.doOperation(request)
            else:
                print("Reconnection failed three times - giving up")
                return None
            
        except Exception as e: 
            print(f"Error during doOperation: {e}")
            print(f"What eror is it: {type(e).__name__},{e.args}")

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
        request = {"Operation": "close"}
        self.doOperation(request)
        if self.connected and self.ws is not None:
            self.ws.close()
            self.connected = False
            self.ws = None
        return "Server and client is closed"
        
        