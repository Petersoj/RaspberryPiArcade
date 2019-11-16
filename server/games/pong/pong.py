from typing import List, Tuple
from websockets import WebSocketServer
from ...board.Board import Board
from random import random
import json
import math

class Pong:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.ballPosition: List[float, float] = [width / 2, height / 2]
        self.ballDeltas: Tuple[float, float] = (1, 0.25)
        self.paddles: List[int] = [3, -10, -10, -10]
        self.players: List[WebSocketServer] = [None, None, None, None]
        self.clients: List[WebSocketServer] = []

    async def connect(self, websocket: WebSocketServer):
        self.clients.append(websocket)
        paddleIndex = -1
        for i in range(self.players):
            if self.players[i] is None:
                self.players[i] = websocket
                if i < 2:
                    self.paddles[i] = int(self.width / 2)
                elif i < 4:
                    self.paddles[i] = int(self.height / 2)
                websocket.send(json.dumps({"type": "GAME-ACCEPT", "position": i}))
                return
        websocket.send(json.dumps({"type": "GAME-ACCEPT", "position": -1}))
        if paddleIndex != -1:
            while True:
                message = await websocket.recv()
                try:
                    message = json.load(message)
                    if not message.get("type", None) == "POSITION_CHANGE":
                        continue
                    direction = message.get("direction", None)
                    try:
                        direction = int(direction)
                    except ValueError as err:
                        continue

                    if direction != -1 and direction != 1:
                        continue

                    self.paddles[paddleIndex] += direction

                    if paddleIndex < 2:
                        self.paddles[paddleIndex] = max(1, min(self.height - 2, self.paddles[paddleIndex]))
                    else:
                        self.paddles[paddleIndex] = max(1, min(self.width - 2, self.paddles[paddleIndex]))

                except Exception as e:
                    print(e)
                    continue

    def update(self):
        board: Board = Board(self.width, self.height)
        self.drawPaddles(board, self.paddles)
        self.runBallLogic(board)
        self.publishBoard(board)

    def publishBoard(self, board: Board):
        board.print()
        for client in self.clients:
            if not client is None:
                client.send(json.dumps({"type": "BOARD_UPDATE", "board": board.getBoard()}))

    def runBallLogic(self, board: Board):
        ballPosition = self.ballPosition
        nextBallPosition = self.getNextBallPosition(board)
        nextBallPosition[0] = int(round(nextBallPosition[0]))
        nextBallPosition[1] = int(round(nextBallPosition[1]))

        if board.get(nextBallPosition[0], nextBallPosition[1]):

            if nextBallPosition[0] == 0:
                self.kill(0)
            elif nextBallPosition[1] == self.width - 1:
                self.kill(1)

            if nextBallPosition[1] == 0:
                self.kill(2)
            elif nextBallPosition[1] == self.height - 1:
                self.kill(3)

            if board.get(nextBallPosition[0], ballPosition[1]):
                self.ballDeltas = (self.bounce(self.ballDeltas[0]), self.ballDeltas[1])
            if board.get(ballPosition[0], nextBallPosition[1]):
                self.ballDeltas = (self.ballDeltas[0], self.bounce(self.ballDeltas[1]))
            scale = max(abs(self.ballDeltas[0]), abs(self.ballDeltas[1]))
            self.ballDeltas = (self.ballDeltas[0]/scale, self.ballDeltas[1]/scale)

        ballPosition = self.getNextBallPosition(board)
        self.ballPosition = ballPosition

        print(f"position: {ballPosition}")

        self.ballPosition = ballPosition

        board.write(round(ballPosition[0]), round(ballPosition[1]), True)



    def bounce(self, delta: float) -> float:
        next: float = -delta + (random() - 0.5) / 4
        if delta >= 0:
            print(f"updating positive {delta}")
            return max(min(-0.1, next), -1)
        else:
            print(f"updating negative {delta}")
            return min(max(0.1, next), 1)

    def getNextBallPosition(self, board: Board):
        position: List[float] = []
        position.append(self.ballPosition[0] + self.ballDeltas[0])
        position.append(self.ballPosition[1] + self.ballDeltas[1])
        return position

    def length(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def kill(self, player: int):
        websocket: WebSocketServer = self.players[player]
        self.players[player] = None
        self.paddles[player] = -10
        if not websocket is None:
            websocket.send(json.dumps({"type": "KILL"}))

    def drawPaddles(self, board: Board, paddles: List[int]):
        for index, position in enumerate(paddles):
            base: int = 0
            shiftDirection: int = - (index % 2)
            if index == 1:
                base = self.width - 1
            if index == 3:
                base = self.height - 1
            for offset in range(-1, 2):
                if index < 2:
                    board.write(base, self.height + (position + offset) * shiftDirection, True)
                elif index < 4:
                    board.write(self.width + (position + offset) * shiftDirection, base, True)