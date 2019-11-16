from typing import List
import json

class Board:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.board: List[List[bool]] = []
        for y in range(width):
            row = []
            for x in range(height):
                row.append(False)
            self.board.append(row)

    def write(self, x: int, y: int, value: bool):
        if not self.contains(x, y):
            return
        self.board[y][x] = value

    def get(self, x: int, y: int) -> bool:
        if not self.contains(x, y):
            return True
        return self.board[y][x]

    def contains(self, x:int, y: int):
        return (0 <= x < self.width) and (0 <= y < self.height)

    def getJson(self):
        return json.dump(self.board)