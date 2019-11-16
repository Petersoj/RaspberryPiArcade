import RPi.GPIO as GPIO
from ..board import Board

# See: https://pinout.xyz/#
# (0, 0) is top left of 2D LED matrix
x_pins = [18, 23, 24, 25, 8, 7, 1, 12]
y_pins = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

for x_pin in range(len(x_pins)):
    GPIO.setup(x_pin, GPIO.OUT)

for y_pin in range(len(y_pins)):
    GPIO.setup(y_pin, GPIO.OUT)


def update_led_matrix(board: Board):
    for row in range(board.height):
        for col in range(board.width):
            board_on: bool = board.board[row][col]
            gpio_output = GPIO.HIGH if board_on else GPIO.LOW

            GPIO.output(x_pins[col], gpio_output)
            GPIO.output(y_pins[row], gpio_output)

