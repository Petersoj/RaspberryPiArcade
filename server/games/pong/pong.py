from typing import List, Tuple
from websockets import WebSocketServer
from ...board.Board import Board
from ...leddriver.leddriver import update_led_matrix
from random import random
import json
import math

class Pong:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.ballPosition: List[float, float] = [width / 2, height / 2]
        self.ballDeltas: Tuple[float, float] = (1, 0.33)
        self.paddles: List[int] = [int(height / 2), int(height / 2), -10, -10]
        self.players: List["Player"] = [None, None, None, None]
        self.clients: List[WebSocketServer] = []
        self.running = False

    def start(self):
        self.running = True

    def isRunning(self) -> bool:
        count = 0
        for player in self.players:
            if player is not None:
                count += 1
        print(self.players)
        return count > 1

    def move(self, player: int, direction: int):
        self.paddles[player] = max(1, min(self.paddles[player] + direction, self.width - 2))

    def addPlayer(self, palyer: "Player"):
        for i in range(len(self.players)):
            if self.players[i] is None:
                self.players[i] = palyer
                return

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
        for index, player in enumerate(self.players):
            if player is None:
                continue
            if player.isRightPressed():
                self.move(index, 1)
            if player.isLeftPressed():
                self.move(index, -1)
        board: Board = Board(self.width, self.height)
        self.drawPaddles(board, self.paddles)
        self.runBallLogic(board)
        self.publishBoard(board)

    def publishBoard(self, board: Board):
        update_led_matrix(board)
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

            if nextBallPosition[0] == -1:
                self.kill(0)
            elif nextBallPosition[1] == self.width:
                self.kill(1)

            if nextBallPosition[1] == -1:
                self.kill(2)
            elif nextBallPosition[1] == self.height:
                self.kill(3)

            if board.get(nextBallPosition[0], ballPosition[1]):
                self.ballDeltas = (self.bounce(self.ballDeltas[0]), self.ballDeltas[1])
            if board.get(ballPosition[0], nextBallPosition[1]):
                self.ballDeltas = (self.ballDeltas[0], self.bounce(self.ballDeltas[1]))
            scale = max(abs(self.ballDeltas[0]), abs(self.ballDeltas[1]))
            self.ballDeltas = (self.ballDeltas[0]/scale, self.ballDeltas[1]/scale)

        ballPosition = self.getNextBallPosition(board)
        self.ballPosition = ballPosition

        self.ballPosition = ballPosition

        board.write(round(ballPosition[0]), round(ballPosition[1]), True)



    def bounce(self, delta: float) -> float:
        next: float = -delta + (random() - 0.5) / 4
        if delta >= 0:
            return max(min(-0.1, next), -1)
        else:
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


    def drawPaddles(self, board: Board, paddles: List[int]):
        for index, position in enumerate(paddles):
            base: int = 0
            shiftDirection: int =  -1
            if index == 1:
                shiftDirection = 1
                base = self.width - 1
            if index == 3:
                shiftDirection = 1
                base = self.height - 1
            for offset in range(-1, 2):
                if index < 2:
                    board.write(base, int(abs((position + offset) * shiftDirection)), True)
                elif index < 4:
                    board.write(int(abs((position + offset) * shiftDirection)), base, True)