from server.board.Board import *
from server.leddriver.leddriver import *
import RPi.GPIO as GPIO
import time

size = 0
try:
    while True:
        b = Board(8, 8)
        for i in range(size):
            b.board[i][i] = True

        update_led_matrix(b)
        if is_p2_up():
            size = abs((size + 1) % 8)
        elif is_p2_down():
            size = (size + 7) % 8

        time.sleep(0.1)

except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
