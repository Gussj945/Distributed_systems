import json

class clock: 
    def __init__(self, numberServers, myID): 
        """
        Initializes a vector clock object. 
        Parameter numberServers is the total number of servers that are communicating. 
        Parameter myID is the ID of the server on which the object is created. 
                       It must be in the range 0 <= myID < numberServers. 
        """
        self.numberServers = numberServers
        self.myID = myID
        self.vectorClock = []
        for i in range(numberServers):
            self.vectorClock.append(0)
        
    def print(self):
        """
        Prints the current time as a list.
        """
        
    def eventHappens(self):
        """ 
        Signals that an event has happened on the local server. 
        This increases its element in the time vector. 
        """
        self.vectorClock[self.myID] += 1
        
    def getTimeNoEvent(self):
        """
        Returns the current time as list of the time values per server. 
        This does not change the time. 
        """
        return self.vectorClock
        
    def getTime(self):
        """
        Returns the current time as list of the time values per server. 
        This triggers an event increasing the time for the local server. 
        """
        self.vectorClock[self.myID] += 1 #should the inc be done before the return?
        return self.vectorClock
        
    def updateTime(self, timeFromOtherServer): 
        """
        Updates the current time according to a given time from some other server. 
        This also triggers an event increasing the time for the local server. 
        Parameter newTimeString contains the time from the other server encoded as string. 
        """ # is timeFromOtherServer a string like this "[0 , 0, 0 ,0]?" says list in lab PM
        for i, clock in enumerate(self.vectorClock):
            self.vectorClock[i] = max(clock, timeFromOtherServer[i])
        
        self.vectorClock[self.myID] += 1
        
def equal(time1, time2): 
    """
    Determines for two times if time1 is the same as time2. 
    Parameter time1: First time. It is a list as returned from getTime() or getTimeNoEvent. 
    Parameter time2: Second time. It is a list as returned from getTime() or getTimeNoEvent. 
    Both times must be lists have the same length.
    """
    return time1 == time2
    
def smallerEqual(time1, time2): 
    """
    Determines for two times if time1 is causally smaller or equal than time2. 
    Parameter time1: First time. It is a list as returned from getTime() or getTimeNoEvent. 
    Parameter time2: Second time. It is a list as returned from getTime() or getTimeNoEvent .
    Both times must be lists have the same length.
    """
    #if one element in time1 is bigger we return false
    """for i in range(len(time1)):
        if time1[i] > time2[i]:
            return False
    return True"""

    return all(t1 <= t2 for t1, t2 in zip(time1, time2))


def concurrent(time1, time2): 
    """
    Determines for two times if time1 is causally concurrent to time2. 
    Parameter time1: First time. It is a list as returned from getTime() or getTimeNoEvent. 
    Parameter time2: Second time. It is a list as returned from getTime() or getTimeNoEvent. 
    Both times must be lists have the same length.
    """
    #if neither time1, time2 or time2, time1 is smallerEqual then they are concurrent
    if smallerEqual(time1, time2) == False and smallerEqual(time2, time1) == False:
        return True
    return False
    
def totalOrder(time1, time2): 
    """
    Defines a total order for times. 
    Total order means, that two times are equal or one time is smaller than the other. 
    The function gets two times and compares it.
    Parameter time1: First time. It is a list as returned from getTime() or getTimeNoEvent. 
    Parameter time2: Second time. It is a list as returned from getTime() or getTimeNoEvent. 
    Returns -1 if time1 < time2
             0 if time1 == time2
             1 if time1 > time2 
    """
    if equal(time1,time2):
        return 0
    if smallerEqual(time1, time2):
        return -1 
    if smallerEqual(time2, time1):
        return 1
    
    #here t1 and t2 is concurrent we invent a deterministic order
    #comparison of first element second if first is equal etc
    if time1 < time2:
        return -1
    else:
        return 1

    
    #here we are concurrent
    #invent some order

