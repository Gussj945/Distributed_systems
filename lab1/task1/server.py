import logging
import websockets
import asyncio
from websockets.asyncio.server import serve


logging.basicConfig(
format= "%(asctime)s %(message)s",
level=logging.DEBUG,
)


async def handler(websocket):
    async for message in websocket:
        await websocket.send("pong")


async def main():
    async with serve(handler,"",10000) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
    

