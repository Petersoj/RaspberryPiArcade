import sys
from games.Snake import Snake
from drivers.display.Screen import Screen as ScreenDriver
from drivers.input.Keyboard import Keyboard as KeyboardDriver
from server import Server
from client import Client

for s in sys.argv:
    print(s, end=' ')

DEFAULT_PORT = 9080


if len(sys.argv) > 1:
    if sys.argv[1] == "--client":
        url = "ws://localhost"
        if len(sys.argv) > 2:
            url = sys.argv[2]
        port = DEFAULT_PORT
        if len(sys.argv) > 3:
            try:
                port = int(sys.argv[3])
            except ValueError as err:
                print(f"port must be an integer not '{sys.argv[3]}'")
        client = Client(port, url)
        client.start()
        # width = 8
        # height = 8
        # driver: ScreenDriver = ScreenDriver()
        # driver.open(width, height)
        # Snake(driver, KeyboardDriver(), width, height).start()
    if sys.argv[1] == "--server":
        port = DEFAULT_PORT
        if len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError as err:
                print(f"must be an integer port not {sys.argv[2]}")
        server = Server(port)
        server.start()