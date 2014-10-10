import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 10
GAME_HEIGHT = 8

#### Put class definitions here ####
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        # print type(player.inventory)
        GAME_BOARD.draw_msg("You just acquired a gem!  You have %d items!" %(len(player.inventory)))
        self.board.del_el(self.x, self.y)
        self.board.del_el(player.x, player.y)
        player.board.set_el(self.x, self.y, player)

class GreenGem(Gem):
    IMAGE = "GreenGem"
    NAME = "Emerald"

class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    NAME = "Sunstone"

class BlueGem(Gem):
    IMAGE = "BlueGem"
    NAME = "Sapphire"

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True



class GrassBlock(GameElement):
    IMAGE = "GrassBlock"

class NPC(GameElement):
    IMAGE = "Horns"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("Hello! Watch out for Dragons! You might be safe with gems")

class Water(GameElement):
    IMAGE = "WaterBlock"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("I can't swim! Turn around.")


class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Dragon(GameElement):
    IMAGE = "GreenDragon"
    SOLID = True 
    LIVE = False

    def interact(self, player):
        self.board.draw_msg("Dragon blows fire! You are dead...")
        player.board.del_el(player.x, player.y)
        place_ashes(player.x, player.y)

class GreenDragon(Dragon):
    IMAGE = "GreenDragon"
    SOLID = True

    def interact(self, player):

        for i in player.inventory:
            if i.NAME == "Emerald":
                self.LIVE = True

        if self.LIVE == True:
            self.board.draw_msg("Green Dragon runs away from magic %s" % i.NAME)
            GreenDragon.SOLID = False
            self.board.del_el(self.x, self.y)
            player.board.del_el(player.x, player.y)
            player.board.set_el(self.x, self.y, player)
        else:
           self.board.draw_msg("Green Dragon eats you and poops")
           player.board.del_el(player.x, player.y)
           place_poop(player.x, player.y)                    

class BlueDragon(Dragon):
    IMAGE = "BlueDragon"
    SOLID = True

    def interact(self, player):

        for i in player.inventory:
            if i.NAME == "Sapphire":
                self.LIVE = True

        if self.LIVE == True:
            self.board.draw_msg("Magic %s makes Blue Dragon spontaneously combust" % i.NAME)
            BlueDragon.SOLID = False
            self.board.del_el(self.x, self.y)
            player.board.del_el(player.x, player.y)
            player.board.set_el(self.x, self.y, player)
        else:
           self.board.draw_msg("Blue Dragon freezes you! You are dead...")
           player.board.del_el(player.x, player.y)
           place_icecube(player.x, player.y)

class OrangeDragon(Dragon):
    IMAGE = "OrangeDragon"
    SOLID = True

    def interact(self, player):

        for i in player.inventory:
            if i.NAME == "Sunstone":
                self.board.draw_msg("Magic %s makes Orange Dragon homesick. He flies home." % i.NAME)
                OrangeDragon.SOLID = False
                self.board.del_el(self.x, self.y)
                player.board.del_el(player.x, player.y)
                player.board.set_el(self.x, self.y, player)
            else:
               self.board.draw_msg("Orange Dragon! You are dead...")
               player.board.del_el(player.x, player.y)
               place_ashes(player.x, player.y)  



 
class Ashes(GameElement):
    IMAGE = "Ashes"
    SOLID = True

class IceCube(GameElement):
    IMAGE = "IceCube"
    SOLID = True

class Poop(GameElement):
    IMAGE = "Poop"
    SOLID = True       

class Character(GameElement):
    IMAGE = "Girl"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

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
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                existing_el = self.board.get_el(next_x, next_y)

                if existing_el:
                    existing_el.interact(self)

                elif existing_el and existing_el.SOLID:
                    self.board.draw_msg("There's something in my way!")
                elif existing_el is None or not existing_el.SOLID:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)
                    


####   End class definitions    ####
def place_ashes(x, y):
    ashes = Ashes()
    # place_ashes_position = (x, y)
    GAME_BOARD.register(ashes)
    GAME_BOARD.set_el(x, y, ashes)

def place_poop(x, y):
    poop = Poop()
    # place_ashes_position = (x, y)
    GAME_BOARD.register(poop)
    GAME_BOARD.set_el(x, y, poop)

def place_icecube(x, y):
    icecube = IceCube()
    # place_ashes_position = (x, y)
    GAME_BOARD.register(icecube)
    GAME_BOARD.set_el(x, y, icecube)

def get_wall_positions(x, y):
    # list init to hold position values

    position = []
    temp_pos = []
    # initial values for position x and y
    x_pos = [0, x]
    y_pos = [0, y]

    # x = GAME_WIDTH -1
    # y = GAME_HEIGHT - 1

        #for loop to create a range of numbers for x while y is 0

    for i in y_pos:
        for j in range(x+1):  
            temp_pos = (j, i)
            if temp_pos not in position:
                position.append(temp_pos)
            # else:
            #     continue


    for k in x_pos:
        for n in range(y+1):
            temp_pos = (k, n)
            if temp_pos not in position:
                position.append(temp_pos)
            # else:
            #     continue

    return position




def initialize():
    """Put game initialization code here"""

    # rock_positions = [
    #     (2,1),
    #     (1,2),
    #     (3,2),
    #     (2,3)
    #     ]

    # rocks = []

    # for pos in rock_positions:
    #     rock = Rock()
    #     GAME_BOARD.register(rock)
    #     GAME_BOARD.set_el(pos[0], pos[1], rock)
    #     rocks.append(rock)

    # rocks[-1].SOLID = False

    water_positions = [
        (1,1),
        (1,2),
        (2,1)]

    waterblocks = []
    for wbpos in water_positions:
        water = Water()
        GAME_BOARD.register(water)
        GAME_BOARD.set_el(wbpos[0], wbpos[1], water)
        waterblocks.append(water)


    wall_position = get_wall_positions((GAME_WIDTH-1), (GAME_HEIGHT-1))
    walls = []
    for wpos in wall_position:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(wpos[0], wpos[1], wall)
        walls.append(wall)


    talltree_positions = [
        (1,3),
        (4,5)
        ]

    talltrees = []

    for tpos in talltree_positions:
        talltree = TallTree()
        GAME_BOARD.register(talltree)
        GAME_BOARD.set_el(tpos[0], tpos[1], talltree)
        talltrees.append(talltree)

    guide = NPC()
    GAME_BOARD.register(guide)
    GAME_BOARD.set_el(1, 4, guide)


    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)

    GAME_BOARD.draw_msg("This game is wicked awesome!")

    blue_gem = BlueGem()
    GAME_BOARD.register(blue_gem)
    GAME_BOARD.set_el(3, 1, blue_gem)

    green_gem = GreenGem()
    GAME_BOARD.register(green_gem)
    GAME_BOARD.set_el(2, 3, green_gem)

    green_dragon = GreenDragon()
    GAME_BOARD.register(green_dragon)
    GAME_BOARD.set_el(4, 3, green_dragon)

    blue_dragon = BlueDragon()
    GAME_BOARD.register(blue_dragon)
    GAME_BOARD.set_el(5, 3, blue_dragon)




