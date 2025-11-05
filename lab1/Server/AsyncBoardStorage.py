class storage: 
    def __init__(self): 
        self.messages = []
        
    async def put(self, message): 
        self.messages = self.messages + [message]
       
    async def get(self, index): 
        index = int(index)
        if index >= 0 and index < len(self.messages): 
            return self.messages[index]
        else: 
            raise IndexError #changed to get right return type
            
    async def getNum(self): 
        return len(self.messages)
        
    async def getBoard(self): 
        return self.messages
        
    async def modify(self, index, message): 
        index = int(index)
        self.messages[index] = message
        
    async def delete(self, index): 
        index = int(index)
        self.messages = [self.messages[i] for i in range(len(self.messages)) if i != index]

    async def deleteAll(self): 
        self.messages = []
        
    async def close(self): 
       await self.close()