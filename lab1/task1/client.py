import logging
import websockets
import asyncio
from websockets.asyncio.client import connect



async def connectToServer():
    connection = await connect("ws://localhost:10000/") #connect to server (PORT 10000)
    # Connect to server
    await connection.send("Ping") # Send a message
    response = await connection.recv() # Receive next message
    await connection.close() # Close

    
if __name__ == "__main__":
    asyncio.run(connectToServer())
