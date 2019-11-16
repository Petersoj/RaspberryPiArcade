from server.leddriver.leddriver import *

class Player:

    def player(self, playerNumber: int):
        self.playerNumber: int = playerNumber

    def isRightPressed(self):
        if self.playerNumber == 1:
            return is_p1_up()
        else:
            return is_p2_up()

    def isLeftPressed(self):
        if self.playerNumber == 1:
            return is_p1_down()
        else:
            return is_p2_down()