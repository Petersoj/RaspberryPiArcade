import sys
from games.Snake import Snake
from drivers.display.Screen import Screen as ScreenDriver
from drivers.input.Keyboard import Keyboard as KeyboardDriver

for s in sys.argv:
    print(s, end=' ')

width = 8
height = 8
driver: ScreenDriver = ScreenDriver()
driver.open(width, height)
Snake(driver, KeyboardDriver(), width, height).start()