import asyncio


class storage: 
    def __init__(self, localStorage, serversToInform, ID, coordinatorID): 
        self.messages = []
        self.localStorage = localStorage
        self.serversToInform = serversToInform
        self.myID = ID
        self.coordinatorID = coordinatorID
        self.lock = asyncio.Lock()

    async def notify_proxies(self, request, senderID):
       
        command = request.get("Operation", "").lower()
        tasks = [] 
        async with self.lock:
            #execute locally within the lock
            match command:
                case "put":
                    message = request.get("Message", "")
                    await self.localStorage.put(message, senderID)
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:
                            print(f"ID som läggs till på listan {proxy.MYID}")
                            tasks.append(proxy.put(message, self.myID))
                    
                case "modify":
                    message = request.get("Message", "")
                    index = request.get("Index", "")
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:    
                            tasks.append(proxy.modify(index, message, self.myID))
                   
                case "delete":
                    index = request.get("Index", "")
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:
                            tasks.append(proxy.delete(index, self.myID))
                  
                case "deleteall":
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:    
                            tasks.append(proxy.deleteAll(self.myID))
                case _:
                    return f"Unknown Command {request}"
        try:
            result = await asyncio.gather(*tasks)
            if result != [None,None,None]:
                return result
            else:
                return "Done" 
        except Exception as e:
            print(f"Exception in asyncio.gather in notify proxiex{e}")
            return e 
                
                

    
    async def put(self, message, senderID=0):
                    
        if self.myID == self.coordinatorID and senderID != self.coordinatorID:
            #forward to all servers
            request = {"Operation": "put", "Message": message}
            return await self.notify_proxies(request, self.myID) #senderID
        elif senderID == -1: #change place on this and the next if statement
            #forward to coordinator
            return await self.serversToInform[self.coordinatorID].put(message, senderID)
        elif senderID == self.coordinatorID:# and self.myID != self.coordinatorID:
            #call comes from coordinator execute locally
            return await self.localStorage.put(message, senderID) 

    async def get(self, index, senderID=0): 
        return await self.localStorage.get(index, senderID)
            
    async def getNum(self, senderID=0): 
        return await self.localStorage.getNum(senderID)
    
    async def getBoard(self, senderID=0): 
        result = await self.localStorage.getBoard(senderID)
        return result
    
    async def modify(self, index, message, senderID=0): 
        if senderID == -1:
            #forward to coordinator
            return await self.serversToInform[self.coordinatorID].modify(index, message, self.myID)            
        elif self.myID == self.coordinatorID and senderID != self.coordinatorID:
            #forward to all servers
            request = {"Operation": "modify", "Index": index, "Message": message}
            await self.localStorage.modify(index, message, senderID)
            return await self.notify_proxies(request, self.myID)
        elif senderID == self.coordinatorID:
            #call comes from coordinator execute locally
            return await self.localStorage.modify(index, message, senderID)

    async def delete(self, index, senderID=0): 
        if senderID == -1:
            # this message comes from a client, forward to coordinator
            return await self.serversToInform[self.coordinatorID].delete(index, self.myID)
            # forward to other servers
        elif self.myID == self.coordinatorID and senderID != self.coordinatorID:
            request = {"Operation": "delete", "Index": index}
            await self.localStorage.delete(index, senderID)
            return await self.notify_proxies(request, self.myID)
        elif senderID == self.coordinatorID:
            return await self.localStorage.delete(index, senderID)

    async def deleteAll(self, senderID=0): 
        if senderID == -1:
            # this message comes from a client
            # forward to coordinator
            return await self.serversToInform[self.coordinatorID].deleteAll(self.myID)
            # forward to other servers
        elif self.myID == self.coordinatorID and senderID != self.coordinatorID:
            request = {"Operation": "deleteAll"}
            await self.localStorage.deleteAll(senderID)
            return await self.notify_proxies(request, self.myID)
        elif senderID == self.coordinatorID:
            return await self.localStorage.deleteAll(senderID)

    async def close(self, senderID=0): 
        return await self.localStorage.close(senderID)
