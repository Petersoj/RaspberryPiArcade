import asyncio
import websockets

class Server:

    def __init__(self, port: int):
        self.port = port

    async def onConnect(self, websocket, path):
        print("connecting")

        await websocket.send(f"hello world")

        print("finished connecting")


    def start(self):
        self.server = websockets.serve(self.onConnect, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()