import asyncio
from VectorClock import totalOrder

class storage: 
    def __init__(self, localStorage, serversToInform, ID, vectorClock): 
        self.messages = []
        self.localStorage = localStorage
        self.serversToInform = serversToInform
        self.myID = ID
        self.vectorClock = vectorClock

    async def notify_proxies(self, request, senderID):

        command = request.get("Operation", "").lower()
        tasks = [] 

        match command:
            case "put":
                message = request.get("Message", "")
                for i, proxy in enumerate(self.serversToInform):
                    if i != senderID:
                        tasks.append(proxy.put(message, senderID))
            case "modify":
                message = request.get("Message", "")
                index = request.get("Index", "")
                for i, proxy in enumerate(self.serversToInform):
                    if i != senderID:
                        tasks.append(proxy.modify(index, message, senderID))
            case "delete":
                index = request.get("Index", "")
                for i, proxy in enumerate(self.serversToInform):
                    if i != senderID:
                        tasks.append(proxy.delete(index, senderID))
            case "deleteall":
                for i, proxy in enumerate(self.serversToInform):
                    if i != senderID:
                        tasks.append(proxy.deleteAll(senderID))
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
            
                

    
    async def put(self, message, senderID=0):
        if senderID == -1:
            # this message comes from a client
            # exeute localy
            messageAndTime = []
            timeStamp = self.vectorClock.getTimeShallow()
            messageAndTime.append(timeStamp)
            messageAndTime.append(message)
            
            await self.localStorage.put(messageAndTime, senderID)
            # forward to other servers

            request = {"Operation": "put", "Message": messageAndTime}
            await self.notify_proxies(request, self.myID)
            return "DONE"
        else:
            return await self.localStorage.put(message, senderID)

    async def get(self, index, serverID=0): 
        return await self.localStorage.get(index, serverID)
            
    async def getNum(self, serverID=0): 
        return await self.localStorage.getNum(serverID)
    
    async def getBoard(self, serverID=0): 
        print(f"entering getBoard for server{serverID}")
        result = await self.localStorage.getBoard(serverID)
        print(f"exiting getboard for server{serverID} with result {result}")
        return result
    
    async def modify(self, index, message, serverID=0): #message here is just str
        if serverID == -1:
            # this message comes from a client
            # exeute localy
            oldMsg = await self.get(index, self.myID)
            
            message = [oldMsg[0], message]
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
    
    def compareMessages(m1, m2):
        return totalOrder(m1, m2)
