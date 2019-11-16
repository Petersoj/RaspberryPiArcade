import asyncio
import websockets
from server.games.pong.pong import Pong
from time import sleep
from threading import Thread

class Server:

    def __init__(self, port: int):
        self.port = port
        self.game = Pong(8, 8)

    async def onConnect(self, websocket, path):
        print("connecting")

        await websocket.send(f"hello world")

        print("finished connecting")

        await self.game.connect(websocket)

    def updateGame(self) -> None:
        while True:
            sleep(1)
            self.game.update()


    def start(self):
        self.server = websockets.serve(self.onConnect, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        Thread(target=self.updateGame).start()
        asyncio.get_event_loop().run_forever()