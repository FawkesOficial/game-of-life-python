from time import sleep as wait
from os import system as cmd, name as os_name

clear_cmd = 'cls' if os_name == 'nt' else 'clear'

def debug(text):
    if debug_mode:
        print(text)


class World:
    def __init__(self, width=40, height=20, dead=" ", alive="⬜", refresh_rate=1, clear_screen=True, wait_for_input=False):
        self.width = width
        self.height = height
        self.dead = dead
        self.alive = alive
        self.refresh_rate = refresh_rate
        self.clear_screen = clear_screen
        self.wait_for_input = wait_for_input


        self.grid = [[dead for i in range(self.width)] for j in range(self.height)]


    def screen(self):
        screen_temp = ""
        for line in self.grid:
            screen_temp += "".join(line) + "\n"
        return screen_temp

    def display(self):
        if self.clear_screen:
            self.clear()
        print(self.screen(), flush=True)

    def clear(self):
        cmd(clear_cmd)

    def isAlive(self, position):
        x, y = position
        cell = self.grid[x][y]
        return (cell == self.alive)

    def make_alive(self, position):
        x, y = position
        self.grid[x][y] = self.alive

    def make_dead(self, position):
        x, y = position
        self.grid[x][y] = self.dead

    def no_of_neighbors(self, position):
        neighbors = 0
        x, y = position

        if self.isAlive(((x-1)%self.height, (y-1)%self.width)):
            neighbors += 1
            debug("Top Left alive")
            debug((x, y))
        if self.isAlive(((x-1)%self.height, y)):
            neighbors += 1
            debug("Up alive")
            debug((x, y))
        if self.isAlive(((x-1)%self.height, (y+1)%self.width)):
            neighbors += 1
            debug("Top Right alive")
            debug((x, y))
        if self.isAlive((x, (y-1)%self.width)):
            neighbors += 1
            debug("Left alive")
            debug((x, y))
        if self.isAlive((x, (y+1)%self.width)):
            neighbors += 1
            debug("Right alive")
            debug((x, y))
        if self.isAlive(((x+1)%self.height, (y-1)%self.width)):
            neighbors += 1
            debug("Bottom Left alive")
            debug((x, y))
        if self.isAlive(((x+1)%self.height, y)):
            neighbors += 1
            debug("Down alive")
            debug((x, y))
        if self.isAlive(((x+1)%self.height, (y+1)%self.width)):
            neighbors += 1
            debug("Bottom Right alive")
            debug((x, y))

        return neighbors


    def check(self, position):
        neighbors = self.no_of_neighbors(position)
        if self.isAlive(position):
            if (neighbors < 2) or (neighbors > 3):
                return self.dead
            else:
                return "unchanged"
        else:
            if neighbors == 3:
                return self.alive


    def update(self):
        changes = []
        for x in range(self.height):
            for y in range(self.width):
                position = (x, y)
                changes.append(self.check(position))
                #print((x, y))
        iterator = 0
        for x in range(self.height):
            for y in range(self.width):
                position = (x, y)
                change = changes[iterator]
                if change == self.alive:
                    self.make_alive(position)
                elif change == self.dead:
                    self.make_dead(position)

                iterator += 1

    def start(self):
        try:
            generation = 0

            self.display()
            
            print("Generation:", generation)
            print()
            
            generation += 1
            if self.wait_for_input:
                input("Press enter to continue...")
            else:
                wait(self.refresh_rate)

            while True:

                self.update()
                self.display()

                print("Generation:", generation)
                print()
                
                generation += 1
                if self.wait_for_input:
                    input("Press enter to continue...")
                else:
                    wait(self.refresh_rate)
        except KeyboardInterrupt:
            print("\r[X] Stopped running")
            print()


debug_mode = False

if debug_mode:
    world = World(clear_screen=False, dead="0", alive="1", wait_for_input=True)
else:
    world = World(refresh_rate=0.2)

def make_line():
    world.make_alive((1,1))
    world.make_alive((2,1))
    world.make_alive((3,1))

def make_glider():
    world.make_alive((0, 0))
    world.make_alive((1, 1))
    world.make_alive((1, 2))
    world.make_alive((2, 0))
    world.make_alive((2, 1))

make_glider()

world.start()
