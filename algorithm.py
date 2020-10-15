from config import CFG

import pygame
from queue import PriorityQueue as PrQ
import math
import sys
import time

# ---- A* ALGORITHM ----
def A_star_alg(draw, grid,start,end):
    """
    @param draw: function to draw the algorithm
    @param grid: 2-dimension list with Spot's instances
    @param start: starting node
    @param end: ending node
    @global param in the context: CFG.SLEEP_TIME - define the visualization-delay
    @postcondition: draws the algorithm with 'draw', finds the marks the shortest path (if such path exist)
    """
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
        if CFG.SLEEP_TIME: time.sleep(CFG.SLEEP_TIME)
    return False,-1

def rebuild_the_path(draw,came_from,curr):
    steps=0
    while curr in came_from:
        steps+=1
        curr=came_from[curr]
        curr.mark_path = True
        draw()
    return steps
