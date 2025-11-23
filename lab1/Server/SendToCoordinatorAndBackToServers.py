import asyncio


class storage: 
    def __init__(self, localStorage, serversToInform, ID, coordinatorID): 
        self.messages = []
        self.localStorage = localStorage
        self.serversToInform = serversToInform
        self.myID = ID
        self.coordinatorID = coordinatorID
        self.lock = asyncio.Lock()

    async def make_update_call_servers(self, method_name: str, senderID: int, *parameters):
       
        local_function = getattr(self.localStorage, method_name) 
        task = []
  
        if self.myID == self.coordinatorID and senderID != self.coordinatorID: 
            async with self.lock:
                #the call comes from the client to the coordinator => 
                #make change localy!
                await local_function(*parameters, senderID)
                for i, proxy in enumerate(self.serversToInform):
                    if i != self.myID: 
                        proxy_function = getattr(proxy, method_name)
                        task.append(proxy_function(*parameters, self.myID))
        elif senderID == -1:
            #the call comes from a client => call on the coordinator
                coordinator_proxy = self.serversToInform[self.coordinatorID]
                coordinator_proxy_function = getattr(coordinator_proxy, method_name)
                return await coordinator_proxy_function(*parameters, self.myID)
        elif self.myID != self.coordinatorID:
             #the coordinator is the sender ID => do the cahnges localy
                return await local_function(*parameters, senderID)

        #if we have tasks to execute
        if task:
            try: 
                result = await asyncio.gather(*task)
                if result != [None, None, None]:
                    return result 
                else:
                    return "DONE"
            except Exception as e: 
                print(f"Exception in asyncio.gather in asyncproxies{e}")
                return e

                
                
            

        """ if self.myID == self.coordinatorID and senderID != self.coordinatorID:
            #forward to all servers
            request = {"Operation": "put", "Message": message}
            return await self.make_update_call_servers(request, self.myID)
        elif senderID == -1: #change place on this and the next if statement
            #forward to coordinator
            return await self.serversToInform[self.coordinatorID].put(message, senderID)
        elif senderID == self.coordinatorID:
            #call comes from coordinator execute locally
            return await self.localStorage.put(message, senderID) 
        """

        """  command = request.get("Operation", "").lower()
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
                    await self.localStorage.modify(index, message, senderID)
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:    
                            tasks.append(proxy.modify(index, message, self.myID))
                   
                case "delete":
                    index = request.get("Index", "")
                    await self.localStorage.delete(index, senderID)
                    for i, proxy in enumerate(self.serversToInform):
                        if i != senderID:
                            tasks.append(proxy.delete(index, self.myID))
                  
                case "deleteall":
                    await self.localStorage.deleteAll(senderID)
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
            return e  """
                
                

    
    async def put(self, message, senderID=0):
        
        """   if self.myID == self.coordinatorID and senderID != self.coordinatorID:
                #forward to all servers
                request = {"Operation": "put", "Message": message}
                return await self.make_update_call_servers(request, self.myID)
            elif senderID == -1: #change place on this and the next if statement
                #forward to coordinator
                return await self.serversToInform[self.coordinatorID].put(message, senderID)
            elif senderID == self.coordinatorID:
                #call comes from coordinator execute locally
                return await self.localStorage.put(message, senderID)  """
      
        return await self.make_update_call_servers("put", senderID, message)

    async def get(self, index, senderID=0): 
        return await self.localStorage.get(index, senderID)
            
    async def getNum(self, senderID=0): 
        return await self.localStorage.getNum(senderID)
    
    async def getBoard(self, senderID=0): 
        result = await self.localStorage.getBoard(senderID)
        return result
    
    async def modify(self, index, message, senderID=0): 
        """if self.myID == self.coordinatorID and senderID != self.coordinatorID:
            #forward to all servers
            request = {"Operation": "modify", "Index": index, "Message": message}
            return await self.make_update_call_servers(request, self.myID)
        elif senderID == -1: #change place on this and the next if statement
            #forward to coordinator
            return await self.serversToInform[self.coordinatorID].modify(index, message, senderID)
        elif senderID == self.coordinatorID:
            #call comes from coordinator execute locally
            return await self.localStorage.modify(index, message, senderID) """
        
        return await self.make_update_call_servers("modify", senderID, index, message)

    async def delete(self, index, senderID=0): 

        """ if self.myID == self.coordinatorID and senderID != self.coordinatorID:
                #forward to all servers
                request = {"Operation": "delete", "Index": index}
                return await self.make_update_call_servers(request, self.myID)
            elif senderID == -1: #change place on this and the next if statement
                #forward to coordinator
                return await self.serversToInform[self.coordinatorID].delete(index, senderID)
            elif senderID == self.coordinatorID:
                #call comes from coordinator execute locally
                return await self.localStorage.delete(index, senderID)
            """
        return await self.make_update_call_servers("delete", senderID, index)

        
    async def deleteAll(self, senderID=0): 
        """if self.myID == self.coordinatorID and senderID != self.coordinatorID:
            #forward to all servers
            request = {"Operation": "deleteAll"}
            return await self.make_update_call_servers(request, self.myID)
        elif senderID == -1: #change place on this and the next if statement
            #forward to coordinator
            return await self.serversToInform[self.coordinatorID].deleteAll(senderID)
        elif senderID == self.coordinatorID:
            #call comes from coordinator execute locally
            return await self.localStorage.deleteAll(senderID)"""
        return await self.make_update_call_servers("deleteAll", senderID)


    async def close(self, senderID=0): 
        return await self.localStorage.close(senderID)
