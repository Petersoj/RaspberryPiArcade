from drivers.Driver import Driver
from drivers.input.Keyboard import Keyboard

from typing import List, Dict
from time import sleep

class Snake:

    def __init__(self, drive: Driver, inputDriver: Keyboard, width: int, height: int):
        self.displayDriver: Driver = drive
        self.inputDriver: Keyboard = inputDriver
        self.width: int = width
        self.height: int = height

        self.trailLength = 3
        self.trail: List[Dict[str, int]] = []

        self.facing = 0
        self.x = 3
        self.y = 3

    def start(self):
        while True:
            self.update()
            sleep(1)

    def update(self):
        if len(self.trail) > 0 and len(self.trail) >= self.trailLength:
            dropPosition = self.trail.pop(0)
            self.displayDriver.write(dropPosition.get("x"), dropPosition.get("y"), "#000000")

        if self.inputDriver.isUpPressed():
            self.facing = 3
        elif self.inputDriver.isDownPressed():
            self.facing = 1
        elif self.inputDriver.isLeftPressed():
            self.facing = 0
        elif self.inputDriver.isRightPressed():
            self.facing = 2

        if self.facing % 2 == 0:
            self.x = (self.facing - 1 + self.x + self.width) % self.width
        else:
            self.y = (self.facing - 2 + self.x + self.width) % self.width
        self.trail.append({"x": self.x, "y": self.y})
        self.displayDriver.write(self.x, self.y, "#ffff00")
        self.displayDriver.flush()