# Information on the websocket-client is available at 
# https://websocket-client.readthedocs.io/en/latest/

class storage: 
    def __init__(self, port): 
        self.port = port
       
    def doOperation(self, request): 
        return None
       
    def put(self, message): 
        return None
       
    def get(self, index): 
        return "Not yet implemented"

    def getNum(self): 
        return 0
        
    def getBoard(self): 
        return ["Not yet implemented"]
        
    def modify(self, index, message): 
        return None
        
    def delete(self, index): 
        return None

    def deleteAll(self): 
        return None
        
    def close(self): 
        pass
        