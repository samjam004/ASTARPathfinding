#A* Pathfinding Algorithm in pygame

#Samuel Mount
#Oct 19, 2023

#algorithm pseudocode help from https://www.youtube.com/watch?v=-L-WgKMFuhE
#pygame setup assistance from https://www.youtube.com/watch?v=JtiK0DOeI4A&t=3407s

import pygame 
import math

SCREEN_WIDTH = 700
FPS = 30
TOTAL_ROWS = 50

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (240,255,255)
LIGHT_GREEN = (118,238,198)
DARK_GREEN = (69,139,116)
AQUA = (0,255,255)  
ORANGE = (255,128,0)
GREY = (131,139,139)
CRIMSON = (220,20,60)
GRAPH_GREY = (194,194,194)

class Node:
    def __init__(self, row, col, width, TOTAL_ROWS):
        self.row = row
        self.col = col
        self.width = width
        self.TOTAL_ROWS = TOTAL_ROWS    
        self.color = BLACK
        self.neighbors = []
        self.x = row * width
        self.y = col * width
        self.f_cost = 0
        self.h_cost = 0
        self.g_cost = 0
        self.parent = None

    def set_parent(self, node):
        self.parent = node


    def set_f(self):
        self.f_cost = self.g_cost + self.h_cost

    def set_g(self, parent): 
        row, col = parent.get_pos()

        if row == self.row or col == self.col:  # If neighbor is adjacent
            new_g_cost = parent.get_g() + 10
        else:  # Neighbor is diagonal
            new_g_cost = parent.get_g() + 14

        if new_g_cost < self.g_cost:
            self.g_cost = new_g_cost
            self.parent = parent
            return 1  # Return 1 to indicate that g_cost was updated
        else:
            return 0  # Return 0 to indicate that g_cost was not updated

    def set_h(self, end): #Distance to target node using eucledian distance
        r1, c1 = self.get_pos()
        r2, c2 = end.get_pos()
        self.h_cost = math.floor(math.sqrt(math.pow((r2 - r1), 2) + math.pow((c2 - c1), 2)))

    def get_f(self):
        return self.f_cost

    def get_g(self):
        return self.g_cost

    def get_h(self):
        return self.h_cost

    def get_pos(self):
        return self.row, self.col
    
    def get_color(self): #debug
        return self.color

    def draw_node(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width - 1, self.width -1))
    
    def make_barrier(self):
        self.color = GREY
    
    def reset(self):
        self.color = BLACK

    def make_start(self):
        self.color = AQUA
    
    def make_end(self):
        self.color = CRIMSON

    def make_open(self):
        self.color = LIGHT_GREEN

    def make_closed(self):
        self.color = DARK_GREEN

    def make_path(self):
        self.color = ORANGE

    def is_barrier(self):
        return self.color == GREY
    
    def is_end(self):
        return self.color == CRIMSON

    def is_open(self):
        return self.color == LIGHT_GREEN

    def is_closed(self):
        return self.color == DARK_GREEN

    def is_path(self):  
        return self.color == ORANGE
    
    def is_start(self):
        return self.color == AQUA

    def is_end(self):
        return self.color == CRIMSON

    def update_neighbors(self, grid): 
        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if i >= 0 and j >= 0:
                    if i != self.row or j != self.col:
                        grid[i][j].set_g(self) 
                        self.neighbors.append(grid[i][j])




    
    def get_neighbors(self):
        return self.neighbors

    def __lt__(self, other):
        return self.f_cost < other.get_f()

def heuristic(point_1, point_2):
    x1, y1 = point_1.get_pos()
    x2, y2 = point_2.get_pos()
    return (x1 - x2) + (y1 - y2)

def grid(desired_rows, screen_width):
    grid = []
    cube_width = screen_width/desired_rows
    for i in range(desired_rows):
        grid.append([])
        for j in range(desired_rows):
            node = Node(i, j, cube_width, desired_rows)
            grid[i].append(node)
    return grid

def draw(screen, grid):
    screen.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw_node()

    pygame.display.update()

def get_clicked_pos(mouse_position, rows, width):
    cube_width = width // rows
    x, y = mouse_position

    row = x // cube_width
    col = y // cube_width

    return row, col

def a_star(grid, start, end):
    open_nodes = []
    closed_nodes = []
    open_nodes.append(start)
    path_found = False

    while not path_found:
        clock.tick(15)
        draw(screen, new_grid)
        current = min(open_nodes)   
        current.update_neighbors(new_grid)
        index = open_nodes.index(current)
        open_nodes.pop(index)
        closed_nodes.append(current)
        current.make_closed()
        
        if current is end:
            path_found = True
            print("Path Found")

        for neighbor in current.get_neighbors():
            if neighbor in closed_nodes:  # Skip nodes in the closed set and barriers
                continue

            if neighbor.is_barrier():
                continue

            if neighbor.set_g(current) == 1 or neighbor not in open_nodes:
                neighbor.set_g(current)
                neighbor.set_h(end)
                neighbor.set_f()

                if neighbor not in open_nodes:
                    open_nodes.append(neighbor)
                    neighbor.make_open()

        print("loop completed")

    print("complete")




new_grid = grid(TOTAL_ROWS, SCREEN_WIDTH)
def main():

    start = None
    end = None
    run = True
    started = False


    while run:
        draw(screen, new_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: 
                mouse_position = pygame.mouse.get_pos()
                x, y = get_clicked_pos(mouse_position, TOTAL_ROWS, SCREEN_WIDTH)
                node = new_grid[x][y]
                if start is None:
                    start = node
                    node.make_start()
                elif end is None:
                    end = node
                    node.make_end()
                else: 
                    if not node.is_end() and not node.is_start():
                        node.make_barrier()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                started = True
                a_star(new_grid, start, end)
                print("success!")

                




main()
pygame.quit()
