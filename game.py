import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"

class Character(GameElement):
    IMAGE = "Girl"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None


    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            direction = "up"
            self.board.draw_msg('%s says: "You pressed up!"' % self.IMAGE)
        elif symbol == key.SPACE:
            direction = "no direction"
            self.board.erase_msg()
        elif symbol == key.DOWN:
            direction = "down"
            self.board.draw_msg('%s says: "You pressed down!"' % self.IMAGE)
        elif symbol == key.LEFT:
            direction = "left"
            self.board.draw_msg('%s says: "You pressed left!"' % self.IMAGE)
        elif symbol == key.RIGHT:
            direction = "right"
            self.board.draw_msg('%s says: "You pressed right!"' % self.IMAGE)

        if direction:
            next_location = self.next_pos(direction)
            next_x = next_location[0]
            next_y = next_location[1]

            self.board.del_el(self.x, self.y)
            self.board.set_el(next_x, next_y, self)


####   End class definitions    ####




def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
        ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

        player = Character()
        GAME_BOARD.register(player)
        GAME_BOARD.set_el(2, 2, player)



