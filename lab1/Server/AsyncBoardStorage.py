class storage: 
    def __init__(self): 
        self.messages = []
        
    async def put(self, message, serverID=0): 
        self.messages = self.messages + [message]
       
    async def get(self, index, serverID=0): 
        index = int(index)
        if index >= 0 and index < len(self.messages): 
            return self.messages[index]
        else: 
            raise IndexError #changed to get right return type
            
    async def getNum(self, serverID=0): 
        return len(self.messages)
        
    async def getBoard(self, serverID=0): 
        return self.messages
        
    async def modify(self, index, message, serverID=0): 
        index = int(index)
        self.messages[index] = message
        
    async def delete(self, index, serverID=0): 
        index = int(index)
        self.messages = [self.messages[i] for i in range(len(self.messages)) if i != index]

    async def deleteAll(self, serverID=0): 
        self.messages = []
        
    async def close(self, serverID=0): 
       await self.ws.close() #not used as of now