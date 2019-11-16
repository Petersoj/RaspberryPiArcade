import keyboard
from drivers.display.Screen import Screen

class Keyboard:

    def open(self):
        pass

    @staticmethod
    def _keyDown(event):
        print(f"pressed key '{event.char}'")

    @staticmethod
    def _keyUp(event):
        print(f"released key '{event.char}'")

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