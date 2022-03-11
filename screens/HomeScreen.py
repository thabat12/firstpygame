import pygame

from internal.PygameApp import PygameApp, Screen
from widgets.BasicMenuBar import BasicMenuBar

# screen paths here
from screens.MapMakerScreen import map_maker_screen

clock = pygame.time.Clock()
size, screen = None, None


def action(size, screen):
    print('action executed')


'''
    @PygameApp:
        Creates the window and initializes everything for you
        Supports function based windows that can be added on to each other

    @Screen:
        Verifies that the function parameters are set correctly
        Validates the new function-based screen
'''


@PygameApp
@Screen
def main_screen(sizep=None, screenp=None):
    size, screen = sizep, screenp
    print(f'this is the current screen {screen}')

    menu_width, menu_height = 600, 300
    menu_rect = pygame.rect.Rect(size[0] // 2 - menu_width // 2, size[1] // 2 - menu_height // 2, menu_width,
                                 menu_height)

    menu = BasicMenuBar(
        screen=screen, menu_width=menu_width,
        menu_height=menu_height, menu_items=['new game', 'load game', 'map maker', 'quit'],
        menu_actions=[action, action, map_maker_screen, pygame.quit], menu_items_color=(100, 50, 100), active_color=(100, 0, 0),
        spacing=1.5
    )

    menu.render()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu.set_active(where=1)
                elif event.key == pygame.K_UP:
                    menu.set_active(where=-1)
                elif event.key == pygame.K_SPACE:
                    menu.execute_action(size, screen)

        screen.fill((0, 0, 0))
        menu.render()
        pygame.display.flip()
