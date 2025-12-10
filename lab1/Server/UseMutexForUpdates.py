import asyncio

class storage: 
    def __init__(self, messageBoard, proxies, myID, leaderElection): 
        self.messageBoard = messageBoard
        self.proxies = proxies
        self.myID = myID
        self.leaderElection = leaderElection
        self.requestQueue = asyncio.Queue()
        self.worker_task = None
        

    async def ensureWorkerRunning(self):
        if self.worker_task is None:
            self.worker_task = asyncio.create_task(self.executeQueue())


    async def executeAndQueue(self, operation_name, senderID=0, *request):
        #coordinator = await self.leaderElection.getCoordinator()
        #coordinatorID = coordinator.MYID
        if senderID == -1:
            await self.ensureWorkerRunning()
            request_tuple = (operation_name, *request)
            await self.requestQueue.put(request_tuple)
        else: 
            #we only enter here if a mutex call has been aquired in executeQueu
            local_func = getattr(self.messageBoard, operation_name)
            await local_func(*request, senderID)

    async def executeQueue(self):
        while True:
            request = await self.requestQueue.get()
            command = request[0] #might be problem for deleteAll who only has arg "deleteAll"
            
            coordinator = await self.leaderElection.getCoordinator()

            if coordinator is None:
                print("No coordinator found")
                self.requestQueue.task_done()
                continue

            acquired = False
            while not acquired:
                acquired = await coordinator.acquire()
                if not acquired:
                    await asyncio.sleep(0.1)

            #Entering critical section
            try:
                tasks = []
                local_function = getattr(self.messageBoard, command)

                await local_function(*request[1:], self.myID) # request[0] is function name await local_function(self.myID, *request[1:])
                for i, proxy in enumerate(self.proxies):
                    if i != self.myID:
                        proxy_function = getattr(proxy, command)
                        tasks.append(proxy_function(*request[1:], self.myID)) 
                if tasks:
                    await asyncio.gather(*tasks)

            except Exception as e:
                print("updateTask - Exception was received.", type(e).__name__, e.args)

            finally: 
                await coordinator.release()
                self.requestQueue.task_done()




    async def put(self, message, senderID=0):
        return await self.executeAndQueue("put", senderID, message)
     
        
    async def get(self, index, senderID=0): 
        return await self.messageBoard.get(index)
            
    async def getNum(self, senderID=0): 
        return await self.messageBoard.getNum()
        
    async def getBoard(self, senderID=0): 
        return await self.messageBoard.getBoard()
        
    async def modify(self, index, message, senderID=0): 
        return await self.executeAndQueue("modify", senderID, index, message)
       
        
    async def delete(self, index, senderID=0): 
        return await self.executeAndQueue("delete", senderID, index)
        
            
    async def deleteAll(self, senderID=0): 
        return await self.executeAndQueue("deleteAll", senderID)
        
        
    async def close(self): 
        self.messageBoard.close()
        for proxy in self.proxies:
            proxy.close()