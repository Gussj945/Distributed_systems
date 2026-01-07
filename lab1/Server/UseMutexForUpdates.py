""" import asyncio

class storage: 
    def __init__(self, messageBoard, proxies, myID, leaderElection): 
        self.messageBoard = messageBoard
        self.proxies = proxies
        self.myID = myID
        self.leaderElection = leaderElection
        self.requestQueue = asyncio.Queue()
        self.worker_task = None
        self.worker_lock = asyncio.Lock()

    async def ensureWorkerRunning(self):
    
        async with self.worker_lock:
            if self.worker_task is None or self.worker_task.done():
                self.worker_task = asyncio.create_task(self.executeQueue()) 


    async def executeAndQueue(self, operation_name, senderID=0, *request):
            # Call from non-client
        
            if senderID != -1:
                local_func = getattr(self.messageBoard, operation_name)
                await local_func(*request, senderID) #senderID
                return
            
            
            coordinator = await self.leaderElection.getCoordinator()
            # Call from client that isn't the coordinator
            if self.myID != coordinator.myID:
                coordinatorProxy = self.proxies[coordinator.myID]
                useMutexForUpdatesFunction = getattr(coordinatorProxy, operation_name)
                await useMutexForUpdatesFunction(*request, senderID)
                return
            
            # Call from client that is the coordinator 
            request_tuple = (operation_name, *request)
            await self.ensureWorkerRunning()
            await self.requestQueue.put(request_tuple)
    


    
    

        
        
    

    
async def executeQueue(self):
    
    try:
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
    except Exception as e:
        print("updateTask - Exception was received.", type(e).__name__, e.args)


    async def executeAndQueue(self, operation_name, senderID=0, *args):

        # Called from another server → just apply locally
        if senderID != -1:
            local_func = getattr(self.messageBoard, operation_name)
            await local_func(*args, senderID)
            return

        # Called from client

        coordinator = await self.leaderElection.getCoordinator()
        
        # Forward to coordinator if I'm not it
        if coordinator.myID != self.myID:
            coordinator_proxy = self.proxies[coordinator.myID]
            coord_proxy_func = getattr(coordinator_proxy, operation_name)
            await coord_proxy_func(*args, senderID=-1)
            return

        # I am coordinator → enqueue
        await self.ensureWorkerRunning()   
        
        acquired = False
        while not acquired:
            acquired_request = await coordinator.acquire()
            acquired = acquired_request["Result"]

            if not acquired:
                await asyncio.sleep(0.05)

        
        await self.requestQueue.put((operation_name, *args))
        #await coordinator.release()
        return

        # no acquire here
        await self.ensureWorkerRunning()   
        await self.requestQueue.put((operation_name, *args))
            
    async def executeQueue(self):
        while True:
            request = await self.requestQueue.get()
            command = request[0]

            try:
                coordinator = self.proxies[self.myID]

                # acquire mutex
                acquired = False
                while not acquired:
                    acquired_request = await coordinator.acquire()
                    acquired = acquired_request["Result"]

                    if not acquired:
                        await asyncio.sleep(0.05)
                
                # local update
                local_func = getattr(self.messageBoard, command)
                await local_func(*request[1:], self.myID)

                # update all other servers
                tasks = []
                for i, proxy in enumerate(self.proxies):
                    if i != self.myID:
                        proxy_func = getattr(proxy, command)
                        tasks.append(proxy_func(*request[1:], self.myID))

                if tasks:
                    await asyncio.gather(*tasks)

            except Exception as ex:
                print("updateTask - Exception was received.",
                    type(ex).__name__, ex.args)

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
            proxy.close()  """

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
            # assert that aquired isnt a string "ERROR"
            acquired = False
            while not acquired:
                acquired_request = await coordinator.acquire()
                if acquired_request["Result"] == True:
                    acquired = True
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