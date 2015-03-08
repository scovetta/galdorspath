import curses
import random
import time

import logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)

def bracket(x, xmin, xmax):
    if x < xmin:
        return xmin
    if x > xmax:
        return xmax
    return x


class GameObject(object):
    def __init__(self, map_object):
        self.screen = map_object.screen
        self.x = 0
        self.y = 0
        self.map = map_object

    # No-Op implementation for the base object
    def turn(self):
        return True

    def __str__(self):
        return "."


class MonsterObject(GameObject):
    def __init__(self, map_object):
        super(MonsterObject, self).__init__(map_object)

    def turn(self):
        r = random.randrange(1, 5)
        if r == 1:
            pass
        elif r == 2:
            self.x += 1 if self.x < self.screen.getmaxyx()[1] else 0
        elif r == 3:
            self.x -= 1 if self.x > 1 else 0
        elif r == 4:
            self.y += 1 if self.y < self.screen.getmaxyx()[0] else 0
        elif r == 5:
            self.y -= 1 if self.y > 1 else 0

        return True

    def __str__(self):
        return "M"

class PlayerObject(GameObject):
    def __init__(self, map_object):
        super(PlayerObject, self).__init__(map_object)

    def turn(self):
        ch = self.screen.getch()
        if ch != -1:
            if ch == curses.KEY_LEFT:
                self.x = bracket( self.x - 1, 0, self.map.max_x)
            elif ch == curses.KEY_RIGHT:
                self.x = bracket( self.x + 1, 0, self.map.max_x)
            elif ch == curses.KEY_UP:
                self.y = bracket( self.y - 1, 0, self.map.max_y)
            elif ch == curses.KEY_DOWN:
                self.y = bracket( self.y + 1, 0, self.map.max_y)
            logging.debug("MOVE PLAYER TO %d, %d" % (self.x, self.y))
            self.map.draw_object_at(self.x, self.y, self)
    def __str__(self):
        return "@"


class Map:
    """ Create a random map """
    def __init__(self, screen):
        self.screen = screen
        self.max_y, self.max_x = 10, 20 #screen.getmaxyx()
        logging.debug("Max Y=%d, Max X=%d" % (self.max_y, self.max_x))
        self.map = []
        for tx in range(self.max_x):
            tobj = []
            for ty in range(self.max_y):
                tobj.append(GameObject(self))
            self.map.append(tobj)

        # Add non-background things to another list
        self.objects = []
        player = PlayerObject(self)
        player.x = 5
        player.y = 5
        self.objects.append(player)

    def display(self):

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                self.draw_object_at(x, y, self.map[x][y], refresh=True)

        for obj in self.objects:
            obj.turn()

    def draw_object_at(self, x, y, obj, refresh=True):
        self.screen.addch(y, x, str(obj))
        if refresh: self.screen.refresh()

    def get_input(self):
        ch = self.screen.getch()
        if ch == -1:
            return False
        else:
            return ch

def main(screen):
    curses.curs_set(0)

    map = Map(screen)

    while(True):
        map.display()
        input = map.get_input()
        #time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)
