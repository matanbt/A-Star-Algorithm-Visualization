import pygame
from config import *

class Spot:
    # i , j = spot's indices in grid
    def __init__(self, i, j):
        self.blocked, self.start, self.end, self.checking, self.checked, self.mark_path = \
            False, False, False, False, False, False
        self.y, self.x = i * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE / 2, j * CFG.SQUARE_SIZE + CFG.SQUARE_SIZE / 2
        self.row, self.col = i, j
        self.n_lst = []

    def update_neighbors(self, grid):
        if self.row != 0 and not grid[self.row - 1][self.col].blocked:
            self.n_lst.append(grid[self.row - 1][self.col])  # UP
        if self.row != len(grid) - 1 and not grid[self.row + 1][self.col].blocked:
            self.n_lst.append(grid[self.row + 1][self.col])  # DOWN

        if self.col != 0 and not grid[self.row][self.col - 1].blocked:
            self.n_lst.append(grid[self.row][self.col - 1])  # LEFT
        if self.col != len(grid[self.row]) - 1 and not grid[self.row][self.col + 1].blocked:
            self.n_lst.append(grid[self.row][self.col + 1])  # RIGHT

    # heuristic func
    def h(self, end):
        if CFG.DIJKSTRA:
            return 0
        else:
            return abs(self.x - end.x) + abs(self.y - end.y)  # Manhattan  Metric
        # return math.sqrt((self.x-end.x)**2 + (self.y-end.y)**2) - Euclidean Metric - DOES NOT work well in grid

    def __lt__(self, other):
        return False  # make spot dummy-comparable to allow tuple use in heap


# GRID
class Grid:
    """represents pygame's main view for algorithms visualization"""

    def __init__(self):
        self.grid = []
        for i in range(CFG.WIDTH_BY_GRIDS):
            self.grid.append([])
            for j in range(CFG.WIDTH_BY_GRIDS):
                self.grid[i].append(Spot(i, j))

    def update_neighbors_all(self):
        for i in range(CFG.WIDTH_BY_GRIDS):
            for j in range(CFG.WIDTH_BY_GRIDS):
                self.grid[i][j].update_neighbors(self.grid)

    # Draws:
    def draw_grid_lines(self):
        for i in range(CFG.WIDTH_BY_GRIDS):
            pygame.draw.line(CFG.SCREEN, GRID_LINES_COLOR, (0, i * CFG.SQUARE_SIZE),
                             (CFG.SQUARE_SIZE * CFG.WIDTH_BY_GRIDS,
                              i * CFG.SQUARE_SIZE))
        for j in range(CFG.WIDTH_BY_GRIDS):
            pygame.draw.line(CFG.SCREEN, GRID_LINES_COLOR, (j * CFG.SQUARE_SIZE, 0), (j * CFG.SQUARE_SIZE,
                                                                                      CFG.SQUARE_SIZE * CFG.WIDTH_BY_GRIDS))

    def draw_grid(self):
        for i in range(CFG.WIDTH_BY_GRIDS):
            for j in range(CFG.WIDTH_BY_GRIDS):
                self.update_spot(self.grid[i][j])
        self.draw_grid_lines()
        pygame.draw.rect(CFG.SCREEN, BAR_COLOR, [0, CFG.WIDTH - 1, CFG.WIDTH, 2])
        pygame.display.update()

    def getSpot(self, i, j):
        return self.grid[i][j]

    # pygame helpers:
    def update_spot(self, spot):
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

        pygame.draw.rect(CFG.SCREEN, color, [spot.col * CFG.SQUARE_SIZE, spot.row * CFG.SQUARE_SIZE,
                                             CFG.SQUARE_SIZE, CFG.SQUARE_SIZE])

    def draw_text(self, text, size=int(1.5 * CFG.SQUARE_SIZE),
                  coor=(CFG.WIDTH // 2, CFG.WIDTH + int(CFG.SQUARE_SIZE * 1.5)),
                  font_name="Comic Sans MS", background=True, bold=True, color=TEXT_COLOR):
        if background: pygame.draw.rect(CFG.SCREEN, BAR_COLOR, [0, CFG.WIDTH - 1, CFG.WIDTH, 3 * CFG.SQUARE_SIZE])
        font = pygame.font.SysFont(font_name, size, bold)
        mytext = font.render(text, True, color)
        rect = mytext.get_rect()
        rect.center = coor  # puts text in coor center
        CFG.SCREEN.blit(mytext, rect)
        pygame.display.update()

    def getMatrix(self):
        #returns the matrix grid, can be mutated
        return self.grid

