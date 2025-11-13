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
    def __init__(self, port, ID=0): 
        self.port = port
        self.url = f"ws://localhost:{self.port}"
        self.ws = None
        self.connected = False
        self.endConnection = False
        self.lock = asyncio.Lock()
        self.MYID = ID

    async def connect(self):
        if self.connected == False:
            self.ws = await websockets.connect(self.url)
            self.connected = True
       
    async def doOperation(self, request): 
        try: 
            async with self.lock:
                if not self.connected and not self.endConnection:
                    await self.connect()
                
                await self.ws.send(json.dumps(request))

                response_string = await self.ws.recv()

                return json.loads(response_string)
                
        
        except Exception as e: 
            print(f"Error during doOperation: {e}")

    async def put(self, message, senderID): 
        request = {"Operation": "put", "Message": message, "MYID": senderID}
        return await self.doOperation(request)

       
    async def get(self, index): 
        request = {"Operation": "get", "Index": index, "MYID": self.MYID}
        return await self.doOperation(request)

    async def getNum(self): 
        request = {"Operation": "getNum", "MYID": self.MYID}
        return await self.doOperation(request)
        
    async def getBoard(self): 
        request = {"Operation": "getBoard", "MYID": self.MYID}
        return await self.doOperation(request)
        
    async def modify(self, index, message): 
        request = {"Operation": "modify", "Index": index, "Message": message, "MYID": self.MYID}
        return await self.doOperation(request)
        
    async def delete(self, index): 
        request = {"Operation": "delete", "Index": index, "MYID": self.MYID}
        return await self.doOperation(request)

    async def deleteAll(self): 
        request = {"Operation": "deleteAll", "MYID": self.MYID}
        return await self.doOperation(request)
        
    async def close(self): 
        request = {"Operation": "close"}
        try:
            # Only try if still connected
            if self.connected and self.ws is not None:
                self.ws.send(json.dumps(request))
                # optionally try to receive a response, but ignore if fails
                # avoid connection closed error
                try:
                    _ = self.ws.recv()
                except Exception:
                    pass
        except Exception:
            pass

        # Close local connection
        if self.connected and self.ws is not None:
            self.ws.close()
        self.connected = False
        self.ws = None
        return "Server and client are closed"


        