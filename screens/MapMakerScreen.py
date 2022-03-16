import pygame, sys, os
# sys.path.append(os.getcwd())
from internal.PygameApp import Screen, Graphic
from widgets.BasicMenuBar import BasicMenuBar
from widgets.BasicButton import BasicButton

clock = pygame.time.Clock()


'''
    Map Maker screen structure:
        - sidebar with menu options
        - toggle select different block types
            - from selection, we can manipulate what is actually being made on the map

    this thing will immediately anchor itself to the top corner of screen
'''
class MapMakerPane:
    def __init__(self, dims, screen, sprite_folder=None, background_color=(255,255,255)):
        self.width = dims[0] if dims[0] >= 1 else screen.width * dims[0]
        self.height = dims[1] if dims[1] >= 1 else screen.height * dims[1]
        self.sprite_folder = sprite_folder
        self.background_color = background_color

        # make some default graphics here
        if not self.sprite_folder:
            pass
        pass


def action():
    print('action time!')


@Screen
def map_maker_screen(size, screen):
    menu = BasicMenuBar(
        screen, 100, 100, menu_items=['reset', 'load', 'save', 'back'], menu_actions=[action, action, action, action],
        font_color=(255, 255, 255, 0), font_size=15, menu_background_color=(0, 0, 0,1)
    )

    btn = BasicButton(
        (100,100), (100,100), action, screen, src='man_idle.png',
        border=5, border_color=(0, 0, 0)
    )

    running = True

    while 1:
        clock.tick(60)

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu.set_active_toggle(1)
                elif event.key == pygame.K_UP:
                    menu.set_active_toggle(-1)
                elif event.key == pygame.K_SPACE:
                    menu.execute_action_toggle()

        menu.render()
        btn.render()

        if running == False:
            break

        pygame.display.flip()

    pygame.quit()
