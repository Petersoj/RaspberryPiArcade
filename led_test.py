from server.leddriver.leddriver import *
import RPi.GPIO as GPIO
import time

size = 6
try:
    while True:
        b = Board(8, 8)
        for x in range(size):
            for y in range(size):
                b.board[x][y] = True

        b.print()
        update_led_matrix(b)

        # if is_p2_up():
        #     size = abs((size + 1) % 8)
        # elif is_p2_down():
        #     size = (size + 7) % 8

        time.sleep(100000)

except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
