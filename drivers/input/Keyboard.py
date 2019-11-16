import keyboard
from drivers.display.Screen import Screen

class Keyboard:

    def open(self, tkDriver: Screen):
        self.tkDriver = tkDriver

    def isUpPressed(self):
        print("up pressed")
        print(keyboard.is_pressed("w"))
        return keyboard.is_pressed("up")

    def isDownPressed(self):
        return keyboard.is_pressed("down")

    def isLeftPressed(self):
        return keyboard.is_pressed("left")

    def isRightPressed(self):
        return keyboard.is_pressed("right")