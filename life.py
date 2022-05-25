from time import sleep as wait
from os import system as cmd, name as os_name

clear_cmd = 'cls' if os_name == 'nt' else 'clear'

def debug(text):
    if debug_mode:
        print(text)


class World:
    def __init__(self, width=40, height=20, dead=" ", alive="⬜", refresh_rate=1, wait_for_input=False):
        self.width = width
        self.height = height
        self.dead = dead
        self.alive = alive
        self.refresh_rate = refresh_rate
        self.wait_for_input = wait_for_input


        self.grid = [[dead for i in range(self.width)] for j in range(self.height)]
        
#         self.grid = []
#         for i in range(self.height):
# #            for j in range(self.width):
#             self.grid.append([dead for j in range(self.width)])



    def display(self):
        screen = ""
        for line in self.grid:
            screen += "".join(line) + "\n"
            #print("".join(line))
        return screen

    def clear(self):
        cmd(clear_cmd)

    def isAlive(self, position):
        cell = self.grid[position[0]][position[1]]
        return cell == self.alive

    def make_alive(self, position):
        self.grid[position[0]][position[1]] = self.alive

    def make_dead(self, position):
        self.grid[position[0]][position[1]] = self.dead

    def no_of_neighbors(self, position):
        neighbors = 0

        #debug((position[0], position[1]))

        if self.isAlive((position[0]-1, position[1]-1)):
            neighbors += 1
            debug("Top Left alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0]-1, position[1])):
            neighbors += 1
            debug("Up alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0]-1, position[1]+1)):
            neighbors += 1
            debug("Top Right alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0], position[1]-1)):
            neighbors += 1
            debug("Left alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0], position[1]+1)):
            neighbors += 1
            debug("Right alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0]+1, position[1]-1)):
            neighbors += 1
            debug("Bottom Left alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0]+1, position[1])):
            neighbors += 1
            debug("Down alive")
            debug((position[0], position[1]))
        if self.isAlive((position[0]+1, position[1]+1)):
            neighbors += 1
            debug("Bottom Right alive")
            debug((position[0], position[1]))

        return neighbors


    def check(self, position):
        if self.isAlive(position):
            if (self.no_of_neighbors(position) < 2) or (self.no_of_neighbors(position) > 3):
                self.make_dead(position)
        else:
            if self.no_of_neighbors(position) == 3:
                self.make_alive(position)
 

    def update(self):
        for x in range(self.height-1):
            for y in range(self.width-1):
                #debug(self.grid[x][y])
                self.check((x, y))


        # for line in self.grid:
        #     for cell in line
        #         self.check()


    def start(self):
        try:
            generation = 0

            #self.clear()
            print(self.display(), flush=True)
            
            print("Generation:", generation)
            print()
            
            generation += 1
            if self.wait_for_input:
                input("Press enter to continue...")
            else:
                wait(self.refresh_rate)

            while True:

                #self.clear()
                self.update()
                print(self.display(), flush=True)
                
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


debug_mode = True

world = World(dead="0", alive="1", wait_for_input=True)

world.make_alive((1,1))
world.make_alive((2,1))
world.make_alive((3,1))

# world.make_alive((1, 1))
# world.make_alive((1, 2))
# world.make_alive((2, 1))
# world.make_alive((2, 2))


world.start()