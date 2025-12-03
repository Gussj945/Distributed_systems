import asyncio

class election: 
    def __init__(self, proxies, myID): 
        """
        Constructs a new object for leader election. 
        Parameter proxies: List with the proxies of all servers ordered by their ID (0, 1, 2, 3, ...)
        Parameter myID: ID of the server in which the object is created. 
        """
        self.proxies = proxies
        self.myID = myID
        self.coordinatorID = None
        
    async def getCoordinator(self): 
        """
        Returns the proxy of the coordinator.
        If there is no coordinator, a new coordinator is elected 
        and the function waits for that.
        Hence it always returns the proxy of a coordinator. 
        """
        return self.proxies[0] # Return the proxy of the coordinator

    async def startElection(self):
        """
        This function starts the election process. 
        When this coroutines ends, a new coordinator has been elected. 
        """
        print("startElection() not implemented.")
        
    async def callAreYouAlive(self, serverID): 
        """
        Calls the function areYouAlive() on the server with the serverID.
        Parameter serverID: ID of the server to check if it is alive. 
        Returns True if the server is alive and False otherwise. 
        """
        response = await self.proxies[serverID].areYouAlive()
        if response == "YES":
            return True
        else:
            return False
            
    async def callElection(self, serverID): 
        """
        Calls the the function election() on the a server with the serverID.
        Parameter serverID: ID of the server in which the method shall be called. 
        Returns the response of the server if the server responded and False otherwise. 
        """        
        try:
            response = await self.proxies[serverID].election()
            return response
        except:
            return False


    async def callSetCoordinator(self, serverID, coordinatorID): 
        """
        Calls the the function setCoordinator() on the a server with the serverID.
        Parameter serverID: ID of the server in which the method shall be called. 
        Parameter coordinatorID: ID of the new coordinator to be announce. 
        Returns True if this was successfull or False if a ConnectionRefusedError was thrown.
        """
        try:
            await self.proxies[serverID].setCoordinator(coordinatorID)
            return True
        except (ConnectionRefusedError):
            return False
        except Exception as e:
            print(f"(LeaderElection callSetCoordinator) What error is it: {type(e).__name__},{e.args}")





        
    async def callSetCoordinatorInAllServers(self, coordinatorID): 
        """ 
        Informs all servers about the new coordinator. 
        Parameter coordinatorID: ID of the new coordinator to be announce. 
        The function is implemented by calling setCoordinator() on all servers.
        """
        tasks = []
        for server_id in range(len(self.proxies)):
            if server_id == self.myID:
                continue
            tasks.append(self.callSetCoordinator(server_id, coordinatorID))

        await asyncio.gather(*tasks)

        

               
                
     
                    
        
    
    ########################################################
    # Methods to be called from other servers via the stub #
    ########################################################
        
    async def election(self):
        """
        Called from other servers to start the election process. 
        Always retuns "Take-Over".
        """
        return "Take-Over"                     
        
    async def setCoordinator(self, coordinatorID):
        """
        Called from to coordinator to inform the server about that it is coordinator. 
        Parameter coordinatorID: ID of the new coordinator. 
        """
        self.coordinatorID = coordinatorID #?
        return f"{coordinatorID} is the new coordinator"
