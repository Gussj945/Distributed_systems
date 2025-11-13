import asyncio


class storage: 
    def __init__(self, localStorage, serversToInform, ID): 
        self.messages = []
        self.localStorage = localStorage
        self.serversToInform = serversToInform
        self.myID = ID


 
    
    async def put(self, message, serverID=0):
        print(f"[Server {self.myID}] PUT called with senderID={serverID}")
        if serverID == -1:
            # this message comes from a client
            # execute localy
            await self.localStorage.put(message, self.myID)
            tasks = []
            for i, proxy in enumerate(self.serversToInform):
                if i != self.myID:
                    tasks.append(proxy.put(message, self.myID))
            print(f"[Server {self.myID}] Created {len(tasks)} proxy tasks")

            results = await asyncio.gather(*tasks, return_exceptions=True)
            print(f"[Server {self.myID}] Proxy results: {results}")
            return "DONE"
        
        else:
            return await self.localStorage.put(message, serverID)



    async def get(self, index, serverID=0): 
        return await self.localStorage.get(index, serverID)
            
    async def getNum(self, serverID=0): 
        return await self.localStorage.getNum(serverID)
    
    async def getBoard(self, serverID=0): 
        return await self.localStorage.getBoard(serverID)
          
    async def modify(self, index, message, serverID=0): 
        return await self.localStorage.modify(index, message, serverID)

    async def delete(self, index, serverID=0): 
        return await self.localStorage.delete(index, serverID)

    async def deleteAll(self, serverID=0): 
        return await self.localStorage.deleteAll(serverID)

    async def close(self, serverID=0): 
        return await self.localStorage.close(serverID)
