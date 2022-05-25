from time import sleep as wait
from os import system as cmd, name as os_name

clear_cmd = 'cls' if os_name == 'nt' else 'clear'

def debug(text):
    if debug_mode:
        print(text)


class World:
    def __init__(self, width=40, height=40, dead="⬛", alive="⬜", refresh_rate=1, clear_screen=True, wait_for_input=False, stop_after_no_changes=False):
        self.width = width
        self.height = height
        self.dead = dead
        self.alive = alive
        self.refresh_rate = refresh_rate
        self.clear_screen = clear_screen
        self.wait_for_input = wait_for_input
        self.stop_after_no_changes = stop_after_no_changes
        self.total_no_of_cells = self.width * self.height


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


        print("Generation:", self.generation, "|", f"Alive Cells: {self.alive_cells}/{self.total_no_of_cells}")


        print()

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
        
        self.alive_cells = 0
        for row in self.grid:
            self.alive_cells += row.count(self.alive)


    def start(self):
        self.generation = 0
        self.alive_cells = 0
        self.stop = False
        try:
            self.display()
            self.generation += 1

            if self.wait_for_input:
                input("Press enter to continue...")
            else:
                wait(self.refresh_rate)

            previous_grids = [str(self.grid)]
            while not self.stop:
                previous_grids.append(str(self.grid))

                self.update()
                self.display()

                if (str(self.grid) == previous_grids[-1] or str(self.grid) == previous_grids[-2]) and self.stop_after_no_changes:
                    self.stop = True

                self.generation += 1
                if self.wait_for_input:
                    input("Press enter to continue...")
                else:
                    wait(self.refresh_rate)
        except KeyboardInterrupt:
            print("\r[X] Stopped running")
            print()

    # Shapes
    def make_still_line(self):
        world.make_alive((1,1))
        world.make_alive((2,1))
        world.make_alive((3,1))

    def make_glider(self):
        world.make_alive((0, 0))
        world.make_alive((1, 1))
        world.make_alive((1, 2))
        world.make_alive((2, 0))
        world.make_alive((2, 1))

    def make_horizontal_glider(self):
        world.make_alive((0, 0))
        world.make_alive((0, 3))
        world.make_alive((1, 4))
        world.make_alive((2, 0))
        world.make_alive((2, 4))
        world.make_alive((3, 1))
        world.make_alive((3, 2))
        world.make_alive((3, 3))
        world.make_alive((3, 4))

    def make_cool_life_starter(self):
        world.make_alive((10, 11))
        world.make_alive((10, 12))
        world.make_alive((11, 10))
        world.make_alive((11, 11))
        world.make_alive((12, 11))

    def make_beehive(self):
        world.make_alive((10,10))
        world.make_alive((10,11))
        world.make_alive((10,12))
        world.make_alive((10,13))

debug_mode = False

if debug_mode:
    world = World(clear_screen=False, dead=" ", alive="X", wait_for_input=True)
else:
    world = World(refresh_rate=1/60, wait_for_input=False, stop_after_no_changes=True)


#world.make_glider()
#world.make_still_line()
#world.make_horizontal_glider()
world.make_cool_life_starter()
#world.make_beehive()

world.start()
