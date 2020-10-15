import sys

from GUI_API import FormGUI
from config import *
from visualization import Grid
from algorithm import A_star_alg


# Pygame Visualization:
def visualization():

    pygame.init()
    pygame.display.set_caption("Matan's A* Algorithm")

    alg_run, start, end = False, None, None
    grid = Grid()
    grid.draw_text("Set: Start, End and Barriers")

    while True:
        grid.draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if not alg_run and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
                pos = pygame.mouse.get_pos()
                if pos[1] >= CFG.WIDTH:
                    continue
                spot = grid.getSpot(pos[1] // CFG.SQUARE_SIZE, pos[0] // CFG.SQUARE_SIZE)
                if pygame.mouse.get_pressed()[0]:
                    if start is None and not spot.end and not spot.blocked:
                        spot.start = True
                        start = spot
                    elif end is None and not spot.start and not spot.blocked:
                        spot.end = True
                        end = spot
                    elif not spot.start and not spot.end:
                        spot.blocked = True

                elif pygame.mouse.get_pressed()[2]:
                    if spot.start:
                        spot.start = False
                        start = None
                    elif spot.end:
                        spot.end = False
                        end = None
                    else:
                        spot.blocked = False

            if not alg_run and event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_SPACE or event.key == pygame.K_BACKSPACE) \
                    and start is not None and end is not None:
                grid.draw_text("Calculating Best Path...", color=CHECKING_COLOR)
                grid.update_neighbors_all()
                alg_run = True
                found, steps = A_star_alg(lambda: grid.draw_grid(), grid.getMatrix(), start, end)
                if found:
                    grid.draw_text("Best Path Found! " + str(steps) + " Steps", color=MARK_PATH_COLOR,
                                   coor=(CFG.WIDTH // 2, CFG.WIDTH + int(CFG.SQUARE_SIZE * 1)))
                else:
                    grid.draw_text("No Path Found!", color=END_COLOR,
                                   coor=(CFG.WIDTH // 2, CFG.WIDTH + int(CFG.SQUARE_SIZE * 1)))

                grid.draw_text("Hit 'A' to Try Again", size=int(0.6 * CFG.SQUARE_SIZE),
                          coor=(CFG.WIDTH // 2, CFG.WIDTH + int(CFG.SQUARE_SIZE * 2.3)), background=False)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                grid.draw_text("Set: Start, End and Barriers")
                start = None
                end = None
                grid = Grid()
                alg_run = False


# Settings Popup:
def settings():
    settings_wind = FormGUI(CFG.setup, title='A* Visualisation Settings', width=460)
    settings_wind.setField('square_size', 'combobox', label='Screen Size', default='MD', values=CFG.SQUARE_SIZE_DICT)
    settings_wind.setField('sleep_time', 'combobox', label='Visualization Speed', default='Normal',
                           values=CFG.SLEEP_TIME_DICT)
    settings_wind.setField('dijkstra', 'combobox', label='Algorithm to Run', default='A* Algorithm',
                           values=CFG.ALGORITHM_CHOICE_DICT)
    settings_wind.run()

# Driver:
if __name__=='__main__':
    settings()
    visualization()
