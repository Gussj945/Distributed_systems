# Information on the websocket-client is available at 
# https://websocket-client.readthedocs.io/en/latest/

import logging
import websockets
import asyncio
import json

logging.basicConfig(
format= "%(asctime)s %(message)s",
level=logging.DEBUG,
) 

class storage: 
    def __init__(self, port, ID=0, logicalClock=None): #should mutex and election be here? should the proxie have a coordinatorID
        self.port = port
        self.url = f"ws://localhost:{self.port}"
        self.ws = None
        self.connected = False
        self.endConnection = False
        self.lock = asyncio.Lock()
        self.MYID = ID
        self.retry = 3
        self.logicalClock = logicalClock
        
        

    async def connect(self):
        if self.connected == False:
            self.ws = await websockets.connect(self.url)
            self.connected = True
  
    async def doOperation(self, request): 
        try: 
            async with self.lock:
                if not self.connected and not self.endConnection:
                    await self.connect()
                if self.logicalClock:
                    timeStamp = request.get("TimeStamp", None)
                    if not timeStamp:
                        request["TimeStamp"] = self.logicalClock.getTime()
                await self.ws.send(json.dumps(request))

                response_string = await self.ws.recv()
                response_dict = json.loads(response_string)
                if self.logicalClock:
                    self.logicalClock.updateTime(response_dict["TimeStamp"])
                return response_dict
        except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
            print(f"connection lost (server side): {e}. Reconnecting...")

            if self.retry > 0: 
                self.connected = False
                await self.connect()
                self.retry -= 1
                return self.doOperation(request)
            else:
                print("Reconnection failed three times - giving up")
                #return None New approach this might break things and require more try/except clauses
                raise ConnectionRefusedError
            
        except Exception as e: 
            print(f"Error during doOperation: {e}")
            print(f"(AsyncBoardProxy) What error is it: {type(e).__name__},{e.args}")

    async def setCoordinator(self, newCoordID, timeStamp=None):
        request = {"Operation": "setCoordinator", "MYID": self.MYID, "newCoordinatorID": newCoordID, "TimeStamp": timeStamp}
        return await self.doOperation(request)

    async def election(self, timeStamp=None):
        request = {"Operation": "election", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)

    async def areYouAlive(self, timeStamp=None):
        request = {"Operation": "areYouAlive", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
    
    async def acquire(self, timeStamp=None):
        request = {"Operation": "acquire", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
    
    async def release(self, timeStamp=None):
        request = {"Operation": "release", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)

    async def put(self, message, senderID, timeStamp=None): 
        request = {"Operation": "put", "Message": message, "MYID": senderID, "TimeStamp": timeStamp} 
        return await self.doOperation(request) #add ID once in doOperation

       
    async def get(self, index, timeStamp=None): 
        request = {"Operation": "get", "Index": index, "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)

    async def getNum(self, timeStamp=None): 
        request = {"Operation": "getNum", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
        
    async def getBoard(self, timeStamp=None): 
        request = {"Operation": "getBoard", "MYID": self.MYID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
        
    async def modify(self, index, message, senderID, timeStamp=None): 
        request = {"Operation": "modify", "Index": index, "Message": message, "MYID": senderID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
        
    async def delete(self, index, senderID, timeStamp=None): 
        request = {"Operation": "delete", "Index": index, "MYID": senderID, "TimeStamp": timeStamp}
        return await self.doOperation(request)

    async def deleteAll(self, senderID, timeStamp=None): 
        request = {"Operation": "deleteAll", "MYID": senderID, "TimeStamp": timeStamp}
        return await self.doOperation(request)
        
    async def close(self, timeStamp=None): 
        request = {"Operation": "close", "TimeStamp": timeStamp}
        try:
            # Only try if still connected
            if self.connected and self.ws is not None:
                await self.ws.send(json.dumps(request))
                # optionally try to receive a response, but ignore if fails
                # avoid connection closed error
                try:
                    _ = await self.ws.recv()
                except Exception:
                    pass
        except Exception:
            pass

        # Close local connection
        if self.connected and self.ws is not None:
            await self.ws.close()
        self.connected = False
        self.ws = None
        return "Server and client are closed"


        #CAN always add timestamp but set its value to None?