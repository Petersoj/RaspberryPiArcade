import asyncio
import websockets

class Client:

    def __init__(self, port: int, url: str):
        self.port: int = port
        self.url: str = url

    async def connect(self):
        uri = self.url + ":" + str(self.port)
        print(uri)
        self.websocket = await websockets.connect(uri)
        await self.websocket.send(f"Hello server")
        print(f"received server response '{await self.websocket.recv()}'")
        while True:
            message = await self.websocket.recv()
            print(message)


    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
        asyncio.get_event_loop().run_forever()