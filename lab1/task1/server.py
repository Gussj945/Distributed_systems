import logging
import websockets
import asyncio
from websockets.asyncio.server import serve
import sys


logging.basicConfig(
format= "%(asctime)s %(message)s",
level=logging.DEBUG,
)

async def forward_ping(other_port):
    try:
        uri = f"ws://localhost:{other_port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send("ping")
            logging.info(f"forwarded ping to {other_port}")
            response = await websocket.recv()
            print(f"message in forward_ping the message from {other_port} is {response}")
            return response
    except Exception as e: 
        logging.exception(f"error in forward_ping: {e}")



async def handler(websocket, other_port=None):
    try:
        async for message in websocket:
            if message == "ping":
                if other_port:
                    pong_msg = await forward_ping(other_port)
                    await websocket.send(pong_msg)
                    logging.info("forwarded pong to ")
                else:
                    await websocket.send("pong")
    except Exception as e: 
        logging.exception(f"error in handler: {e}")


async def main():
    own_port = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    second_port = int(sys.argv[2]) if len(sys.argv) > 2 else None
    async with serve(
        lambda ws: handler(ws, second_port),
        "localhost",
        own_port
    ) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
    

