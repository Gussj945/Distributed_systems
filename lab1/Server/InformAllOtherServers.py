import asyncio


class storage: 
    def __init__(self, localStorage, serversToInform, ID): 
        self.messages = []
        self.localStorage = localStorage
        self.serversToInform = serversToInform
        self.myID = ID

    async def notify_proxies(self, request, senderID):

        command = request.get("Operation", "").lower()
        tasks = [] 

        match command:
            case "put":
                message = request.get("Message", "").lower()
                for i, proxy in enumerate(self.serversToInform):
                    if i != self.myID:
                        tasks.append(proxy.put(message, senderID))
            case "modify":
                message = request.get("Message", "").lower()
                index = request.get("Index", "").lower()
                for i, proxy in enumerate(self.serversToInform):
                    if i != self.myID:
                        tasks.append(proxy.modify(index, message, senderID))
            case "delete":
                index = request.get("Index", "").lower()
                for i, proxy in enumerate(self.serversToInform):
                    if i != self.myID:
                        tasks.append(proxy.delete(index, senderID))
            case "deleteall":
                for i, proxy in enumerate(self.serversToInform):
                    if i != self.myID:
                        tasks.append(proxy.deleteAll(self.myID))
            case _:
                return f"Unknown Command {request}"
        try:
            result = await asyncio.gather(*tasks)
            if result == None:
                return "Done"
            else:
                return result
        except Exception as e:
            print(f"Exception in asyncio.gather in notify proxiex{e}")
            return e
            
                

    
    async def put(self, message, serverID=0):
        if serverID == -1:
            # this message comes from a client
            # exeute localy
            await self.localStorage.put(message, self.myID)
            # forward to other servers
            request = {"Operation": "put", "Message": message}
            await self.notify_proxies(request, self.myID)
            return "DONE"
        else:
            return await self.localStorage.put(message, serverID)

    async def get(self, index, serverID=0): 
        return await self.localStorage.get(index, serverID)
            
    async def getNum(self, serverID=0): 
        return await self.localStorage.getNum(serverID)
    
    async def getBoard(self, serverID=0): 
        print(f"entering getBoard for server{serverID}")
        result = await self.localStorage.getBoard(serverID)
        print(f"exiting getboard for server{serverID} with result {result}")
        return result
    
    async def modify(self, index, message, serverID=0): 
        if serverID == -1:
            # this message comes from a client
            # exeute localy
            result = await self.localStorage.modify(index, message, self.myID)
            # forward to other servers
            request = {"Operation": "modify", "Index": index, "Message": message}
            await self.notify_proxies(request, self.myID)
            return result
        else:
            return await self.localStorage.modify(index, message, serverID)

    async def delete(self, index, serverID=0): 
        if serverID == -1:
            # this message comes from a client
            # exeute localy
            await self.localStorage.delete(index, self.myID)
            # forward to other servers
            request = {"Operation": "delete", "Index": index}
            await self.notify_proxies(request, self.myID)
            return "DONE"
        else:
            return await self.localStorage.delete(index, serverID)

    async def deleteAll(self, serverID=0): 
        if serverID == -1:
            # this message comes from a client
            # exeute localy
            await self.localStorage.deleteAll(self.myID)
            # forward to other servers
            request = {"Operation": "deleteAll"}
            await self.notify_proxies(request, self.myID)
            return "DONE"
        else:
            return await self.localStorage.deleteAll(serverID)

    async def close(self, serverID=0): 
        return await self.localStorage.close(serverID)
