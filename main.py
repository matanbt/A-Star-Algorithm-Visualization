import math
import sys
import time
from queue import PriorityQueue as PrQ
import pygame
from GUI_API import GUIApp

#final vars: (can be modified by user via Settings pop-up)
SQUARE_SIZE=20
SQUARE_SIZE_DICT={
    'SM' : 14, 'MD' : 20, 'LG' : 23,'XL' : 27
}
WIDTH_BY_GRIDS=30
# SQUARE_SIZE , WIDTH_BY_GRIDS=17 , 40

SLEEP_TIME=0
SLEEP_TIME_DICT={
    'Normal': 0, 'Slow' : 0.2, 'Very Slow' : 0.5
}

DIJKSTRA=False
ALGORITHM_CHOICE_DICT = {
    'A* Algorithm':False,'Dijkstra' : True
}

#derived final vars:
WIDTH=SQUARE_SIZE*WIDTH_BY_GRIDS
SCREEN = pygame.display.set_mode((WIDTH,WIDTH+3*SQUARE_SIZE))



#colors:
GRID_LINES_COLOR=(224,224,224)
BG_COLOR=(255,255,255)
BLOCKED_COLOR=(0,0,0)
START_COLOR=(54,210,30)
END_COLOR=(230,43,36)
CHECKING_COLOR=(113,240,255)
CHECKED_COLOR=(20,90,255)
MARK_PATH_COLOR=(163,57,210) # (54,210,30)#

TEXT_COLOR=(255, 255, 255)
BAR_COLOR=(5,20,60)

class Spot:
    #i , j = spot's indices in grid
    def __init__(self,i,j):
        self.blocked,self.start,self.end,self.checking,self.checked,self.mark_path=\
            False,False,False,False,False,False
        self.y,self.x= i*SQUARE_SIZE+SQUARE_SIZE/2 , j*SQUARE_SIZE+SQUARE_SIZE/2
        self.row,self.col=i,j
        self.n_lst = []


    def update_neighbors(self,grid):
        if self.row!=0 and not grid[self.row-1][self.col].blocked:
            self.n_lst.append(grid[self.row-1][self.col]) #UP
        if self.row!=len(grid)-1 and not grid[self.row+1][self.col].blocked:
            self.n_lst.append(grid[self.row+1][self.col]) #DOWN

        if self.col!=0 and not grid[self.row][self.col-1].blocked:
            self.n_lst.append(grid[self.row][self.col-1]) #LEFT
        if self.col!=len(grid[self.row])-1 and not grid[self.row][self.col+1].blocked:
            self.n_lst.append(grid[self.row][self.col+1]) #RIGHT

    #heuristic func
    def h(self,end):
        if DIJKSTRA: return 0
        else: return abs(self.x-end.x) + abs(self.y-end.y) #Manhattan  Metric
        #return math.sqrt((self.x-end.x)**2 + (self.y-end.y)**2) - Euclidean Metric - DOES NOT work well in grid


    def __lt__(self, other):
        return False #will allow tuple use in heap


# ---- A* ALGORITHM ----
#recieves grid of spots (=nodes),start,end and a draw function
def A_star_alg(draw, grid,start,end):
    open_set=PrQ() #minimum heap, key is first tuple's element
    open_set_hash=set() #analog hash-set
    came_from={} #maps nodes to navigation-origin

    g={spot: math.inf for row in grid for spot in row}
    g[start]=0
    f={spot: math.inf for row in grid for spot in row}
    f[start]=g[start]+start.h(end)
    open_set.put((f[start],g[start],start))
    open_set_hash.add(start)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        curr=open_set.get()[2]
        open_set_hash.remove(curr)
        curr.checked=True

        if curr==end:
            steps=rebuild_the_path(draw, came_from, end)
            return True,steps

        for neighbor in curr.n_lst:
            temp_g_score=g[curr]+1 #1 is for the weight of the edge
            if temp_g_score < g[neighbor]:
                #better path found, updates the following
                came_from[neighbor]=curr
                g[neighbor]=temp_g_score
                f[neighbor]=temp_g_score+neighbor.h(end)
                if neighbor not in open_set_hash:
                    open_set.put((f[neighbor],g[neighbor],neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.checking=True

        draw()
        time.sleep(SLEEP_TIME)
    return False,-1

def rebuild_the_path(draw,came_from,curr):
    steps=0
    while curr in came_from:
        steps+=1
        curr=came_from[curr]
        curr.mark_path = True
        draw()
    return steps


#GRID
def init_grid():
    grid=[]
    for i in range(WIDTH_BY_GRIDS):
        grid.append([])
        for j in range(WIDTH_BY_GRIDS):
            grid[i].append(Spot(i,j))
    return grid

def update_neighbors_all(grid):
    for i in range(WIDTH_BY_GRIDS):
        for j in range(WIDTH_BY_GRIDS):
            grid[i][j].update_neighbors(grid)

#Draws:
def draw_grid_lines():
    for i in range(WIDTH_BY_GRIDS):
        pygame.draw.line(SCREEN,GRID_LINES_COLOR,(0,i*SQUARE_SIZE),(SQUARE_SIZE*WIDTH_BY_GRIDS,i*SQUARE_SIZE))
    for j in range(WIDTH_BY_GRIDS):
        pygame.draw.line(SCREEN,GRID_LINES_COLOR,(j*SQUARE_SIZE,0),(j*SQUARE_SIZE,SQUARE_SIZE*WIDTH_BY_GRIDS))

def draw_grid(grid):
    for i in range(WIDTH_BY_GRIDS):
        for j in range(WIDTH_BY_GRIDS):
            update_spot(grid[i][j])
    draw_grid_lines()
    pygame.draw.rect(SCREEN,BAR_COLOR,[0,WIDTH-1,WIDTH,2])
    pygame.display.update()

def update_spot(spot):
    color = BG_COLOR
    if spot.blocked:
        color = BLOCKED_COLOR
    elif spot.start:
        color = START_COLOR
    elif spot.end:
        color = END_COLOR
    elif spot.mark_path:
        color = MARK_PATH_COLOR
    elif spot.checked:
        color = CHECKED_COLOR
    elif spot.checking:
        color = CHECKING_COLOR

    pygame.draw.rect(SCREEN,color,[spot.col*SQUARE_SIZE,spot.row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE])

def draw_text(text, size=int(1.5*SQUARE_SIZE), coor=(WIDTH // 2, WIDTH +int(SQUARE_SIZE*1.5)), font_name="Comic Sans MS",
              background=True, bold=True,color=TEXT_COLOR):
    if background: pygame.draw.rect(SCREEN,BAR_COLOR,[0,WIDTH-1,WIDTH,3*SQUARE_SIZE])
    font = pygame.font.SysFont(font_name, size, bold)
    mytext = font.render(text, True, color)
    rect = mytext.get_rect()
    rect.center = coor  # puts text in coor center
    SCREEN.blit(mytext, rect)
    pygame.display.update()


#MAIN:
def visualization():
    pygame.init()
    pygame.display.set_caption("Matan's A* Algorithm")

    alg_run,start,end=False,None,None
    grid=init_grid()
    draw_text("Set: Start, End and Barriers")

    while True:
        draw_grid(grid)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()

            if not alg_run and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
                pos=pygame.mouse.get_pos()
                spot = grid[pos[1] // SQUARE_SIZE][pos[0] // SQUARE_SIZE]
                if pos[1]>=WIDTH: continue
                elif pygame.mouse.get_pressed()[0]:
                    if start is None and not spot.end and not spot.blocked:
                        spot.start=True
                        start=spot
                    elif end is None and not spot.start and not spot.blocked:
                        spot.end = True
                        end = spot
                    elif not spot.start and not spot.end:
                        spot.blocked=True

                elif pygame.mouse.get_pressed()[2]:
                    if spot.start:
                        spot.start = False
                        start = None
                    elif spot.end:
                        spot.end = False
                        end = None
                    else:
                        spot.blocked=False

            if not alg_run and event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_BACKSPACE)\
                    and start is not None and end is not None:
                draw_text("Calculating Best Path...", color=CHECKING_COLOR)
                update_neighbors_all(grid)
                alg_run=True
                found,steps=A_star_alg(lambda: draw_grid(grid),grid,start,end)
                if found:
                    draw_text("Best Path Found! "+str(steps)+" Steps", color=MARK_PATH_COLOR,coor=(WIDTH // 2, WIDTH +int(SQUARE_SIZE*1)))
                else:
                    draw_text("No Path Found!", color=END_COLOR,coor=(WIDTH // 2, WIDTH +int(SQUARE_SIZE*1)))

                draw_text("Hit 'A' to Try Again",size=int(0.6*SQUARE_SIZE),coor=(WIDTH // 2, WIDTH +int(SQUARE_SIZE*2.3)),background=False)

            elif event.type==pygame.KEYDOWN and event.key==pygame.K_a:
                draw_text("Set: Start, End and Barriers")
                start=None
                end=None
                grid=init_grid()
                alg_run=False

#SETTINGS:
def settings():
    def setup(square_size,sleep_time,dijkstra):
        global SQUARE_SIZE,SLEEP_TIME,DIJKSTRA
        global WIDTH,SCREEN
        SQUARE_SIZE, SLEEP_TIME, DIJKSTRA=square_size,sleep_time,dijkstra
        #re-calculate:
        WIDTH = SQUARE_SIZE * WIDTH_BY_GRIDS
        SCREEN = pygame.display.set_mode((WIDTH, WIDTH + 3 * SQUARE_SIZE))

        visualization()

    settings_wind = GUIApp(setup,title='A* Visualisation Settings',width=460)
    settings_wind.setField('square_size','combobox',label='Screen Size',default='MD',values=SQUARE_SIZE_DICT)
    settings_wind.setField('sleep_time', 'combobox',label='Visualization Speed',default='Normal',
                           values=SLEEP_TIME_DICT)
    settings_wind.setField('dijkstra', 'combobox',label='Algorithm to Run',default='A* Algorithm',
                           values=ALGORITHM_CHOICE_DICT)
    settings_wind.run()

settings()