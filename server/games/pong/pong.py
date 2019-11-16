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
        self.ballPosition: List[int, int] = [int(width / 2), int(height / 2)]
        self.ballDeltas: Tuple[int, int] = (0, 1)
        self.ballDestination: List[int, int] = self.getNextBallDestination(Board(8,8))
        self.paddles: List[int] = [-10, -10, -10, -10]
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
                        print("unknown message type")
                        continue
                    direction = message.get("direction", None)
                    try:
                        direction = int(direction)
                    except ValueError as err:
                        print("direction must be an integer")
                        continue

                    if direction != -1 and direction != 1:
                        print("direction must be -1 or 1")
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
        print("publishing board")
        board.print()
        for client in self.clients:
            if not client is None:
                print("sending to client")
                client.send(json.dumps({"type": "BOARD_UPDATE", "board": board.getBoard()}))

    def runBallLogic(self, board: Board):
        ballPosition: Tuple[int, int] = self.ballPosition
        ballDestination: Tuple[int, int] = self.ballDestination
        if ballPosition[0] == ballDestination[0] and ballPosition[1] == ballDestination[1]:

            if ballPosition[0] == 0:
                self.kill(0)
            elif ballPosition[1] == self.width - 1:
                self.kill(1)

            if ballPosition[1] == 0:
                self.kill(2)
            elif ballPosition[1] == self.height - 1:
                self.kill(3)

        ballPosition = self.ballPosition
        nextBallPosition = self.getNextBallPosition(board)

        if board.get(nextBallPosition[0], nextBallPosition[1]) or (ballPosition[0] == self.ballDestination[0] and ballPosition[1] == self.ballDestination[1]) or ballPosition[0] == 0 or ballPosition[1] == 0 or ballPosition[0] == self.width  - 1 or ballPosition[1] == self.height - 1:
            print(f"orignal deltas: {self.ballDeltas}")
            if ballPosition[0] <= 1 or ballPosition[0] <= self.width - 2 or ballPosition[0] == self.ballDestination[0]:
                self.ballDeltas = (self.bounce(self.ballDeltas[0]), self.ballDeltas[1])
            if ballPosition[1] <= 1 or ballPosition[1] <= self.height - 2 or ballPosition[1] == self.ballDestination[1]:
                self.ballDeltas = (self.ballDeltas[0], self.bounce(self.ballDeltas[1]))
            self.ballDestination = self.getNextBallDestination(board)
            print(f"new deltas: {self.ballDeltas}")

        ballPosition = self.getNextBallPosition(board)
        self.ballPosition = ballPosition

        print(f"position: {ballPosition}")
        print(f"destination: {ballDestination}")

        self.ballPosition = ballPosition

        board.write(ballPosition[0], ballPosition[1], True)



    def bounce(self, delta: float) -> float:
        next: float = -delta + (random() - 0.5) / 8
        if delta >= 0:
            return max(min(-0.1, next), -1)
        else:
            return min(max(0.1, next), 1)

    def getNextBallPosition(self, board: Board):
        minDif: float = 9999999
        position: Tuple[int, int] = (0, 0)
        ballPosition: List[int, int] = self.ballPosition
        ballDestination: Tuple[int, int] = self.ballDestination
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if not board.contains(ballPosition[0] + dx, ballPosition[1] + dy):
                    continue
                dif: float = self.length(ballPosition[0] + dx, ballPosition[1] + dy, ballDestination[0], ballDestination[1])
                if dif < minDif:
                    minDif = dif
                    position = (ballPosition[0] + dx, ballPosition[1] + dy)
        return position

    def getNextBallDestination(self, board: Board):
        ballPosition: List[int, int] = self.ballPosition
        ballDeltas: Tuple[int, int] = self.ballDeltas
        destinationX = ballPosition[0]
        destinationY = ballPosition[1]
        if not ballDeltas[0] == 0:
            if ballDeltas[0] > 0:
                destinationX = int(((self.width - 1) - ballPosition[0]) / ballDeltas[0] + ballPosition[0])
            else:
                destinationX = int(ballPosition[0] + ballPosition[0] / ballDeltas[0])

        if not ballDeltas[1] == 0:
            if ballDeltas[1] > 0:
                print(f"running positive: { ballDeltas[1] / ((self.height - 1) - ballPosition[1]) + ballPosition[1]}")
                destinationY = int(((self.height - 1) - ballPosition[1]) / ballDeltas[1] + ballPosition[1])
            else:
                print(f"running negative: {ballPosition[1] - ballDeltas[1] / ballPosition[1]}")
                destinationY = int(ballPosition[1] - ballPosition[1] / ballDeltas[1])

        return (destinationX, destinationY)




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