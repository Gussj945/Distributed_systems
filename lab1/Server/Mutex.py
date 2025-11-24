class mutex: 
    def __init__(self): 
        self.locked = False
       
        
    async def acquire(self): 
        """
        Acquires the mutex. 
        If the mutex is already aquired, the method returns False. Then a coroutine must not enter its critical section. 
        Returns True, if the mutex was is free. Returns False if the mutex is acquired but not released.
        """
        if self.locked == False:
            print("Entered mutex")
            self.locked = True
            return True
        else: 
            print("Can't enter mutex since another process has entered mutex")
            return False
        
    async def release(self): 
        """
        Frees the mutex. 
        If it is acquired afterwards, method acquire() return True.
        """
        if  self.locked == True:
            print("Exited mutex")
            self.locked = False
            return True
        else: 
            print("Can't release since there wasn't any active mutex")
            return False




