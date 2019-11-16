import RPi.GPIO as GPIO
from ..board import Board

inited = False

# See: https://pinout.xyz/#
# (0, 0) is top left of 2D LED matrix
x_pins = [18, 23, 24, 25, 8, 7, 1, 12]
y_pins = [6, 13, 4, 17, 27, 22, 10, 9]
p1_up_pin = 20
p1_down_pin = 21
p2_up_pin = 19
p2_down_pin = 26

if not inited:
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    for x_pin in range(len(x_pins)):
        print(x_pin)
        GPIO.setup(x_pins[x_pin], GPIO.OUT)

    for y_pin in range(len(y_pins)):
        print(y_pin)
        GPIO.setup(y_pins[y_pin], GPIO.OUT)

    GPIO.setup(p1_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(p1_down_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(p2_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(p2_down_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def update_led_matrix(board: Board):
    for row in range(board.height):
        for col in range(board.width):
            board_on: bool = board.board[row][col]
            gpio_output = GPIO.HIGH if board_on else GPIO.LOW

            GPIO.output(y_pins[row], gpio_output)
            GPIO.output(x_pins[col], gpio_output)


def is_p1_up():
    return GPIO.input(p1_up_pin) == GPIO.HIGH


def is_p1_down():
    return GPIO.input(p1_down_pin) == GPIO.HIGH


def is_p2_up():
    return GPIO.input(p2_up_pin) == GPIO.HIGH


def is_p2_down():
    return GPIO.input(p2_down_pin) == GPIO.HIGH

