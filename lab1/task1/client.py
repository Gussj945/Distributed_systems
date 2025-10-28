import logging
import websockets
import asyncio
from websockets.asyncio.client import connect
import sys

logging.basicConfig(
format= "%(asctime)s %(message)s",
level=logging.DEBUG,
)

async def connectToServer():
    server = sys.argv[1]
    connection = await connect(f"ws://localhost:{server}/") #connect to server 
    # Connect to server
    await connection.send("ping") # Send a message
    response = await connection.recv() # Receive next message
    await connection.close() # Close

    
if __name__ == "__main__":
    asyncio.run(connectToServer())
