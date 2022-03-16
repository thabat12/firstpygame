import pygame
import sys, os

# sys.path.append(os.getcwd())

from internal.PygameApp import PygameApp, Screen
from widgets.BasicMenuBar import BasicMenuBar

# screen paths here
from screens.MapMakerScreen import map_maker_screen

clock = pygame.time.Clock()
size, screen = None, None


def action():
    print('action executed')


'''
    I mainly made these classes for annotations ahead of functions so ik what i'm doing

    @PygameApp:
        Creates the window and initializes everything for you
        Supports function based windows that can be added on to each other

    @Screen:
        Verifies that the function parameters are set correctly
        Validates the new function-based screen
'''


class HomeScreenNavResults:
    mapmaker = 'mapmaker'
    quit = 'quit'
    newgame = 'newgame'
    loadgame = 'loadgame'


def nav_to_newgame():
    return HomeScreenNavResults.newgame


def nav_to_loadgame():
    return HomeScreenNavResults.loadgame


def nav_to_mapmaker():
    return HomeScreenNavResults.mapmaker


def nav_to_quit():
    return HomeScreenNavResults.quit


@PygameApp
@Screen
def main_screen(sizep=None, screenp=None):
    size, screen = sizep, screenp
    print(f'this is the current screen {screen}')

    menu_width, menu_height = 600, 300
    menu_rect = pygame.rect.Rect(size[0] // 2 - menu_width // 2, size[1] // 2 - menu_height // 2, menu_width,
                                 menu_height)
    menu_padding = {
        't': 40,
        'b': 10
    }

    menu_items = ['new game', 'load game', 'map maker', 'quit']
    menu_actions = [nav_to_newgame, nav_to_loadgame, nav_to_mapmaker, nav_to_quit]

    menu = BasicMenuBar(screen, menu_width, menu_height, pos_x=(size[0] // 2) - (menu_width // 2),
                        pos_y=(size[1] // 2) - (menu_height // 2), menu_items=menu_items,
                        menu_actions=menu_actions, menu_title='Welcome!', menu_padding=menu_padding,
                        font_color=(0, 0, 0), font_size=25, title_font_size=35, menu_item_spacing=15, cursor=True)

    running, result = True, None

    while 1:
        clock.tick(60)

        # background
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    result = menu.execute_action_cursor(1)
                    running = False

        menu.render()
        pygame.display.flip()

        if not running and result == HomeScreenNavResults.quit:
            pygame.quit()
            break
        else:
            running = True

        if result == HomeScreenNavResults.mapmaker:
            return map_maker_screen(size, screen)
