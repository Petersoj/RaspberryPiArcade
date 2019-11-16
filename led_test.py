from server.board.Board import *
from server.leddriver.leddriver import update_led_matrix
import time

b = Board(8,8)
update_led_matrix(b)
time.sleep(15)