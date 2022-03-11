import pygame

from internal.PygameApp import Screen
from widgets.BasicMenuBar import BasicMenuBar

clock = pygame.time.Clock()


def action():
    print('action time!')

@Screen
def map_maker_screen(size, screen):
    # keeping track of what matrix values are selected and how far out to go
    matrix_data = set()
    max_x, max_y = size[0], size[1]

    # this is assuming 16:9 aspect ratio... it will always assume that
    box_dims = size[0] // 32

    # scrolling
    offset_x, offset_y = 0, 0

    menu = BasicMenuBar(
        screen, 100, 100, menu_items=['reset', 'load', 'save', 'back'], menu_actions=[action, action, action, action],
        center=False, background_color=(0, 0, 0, 0), ignore_title=True, font_color=(255,255,255),
        spacing=1.1, margin_left=size[0]-100
    )

    running = True

    image = pygame.image.load('../tests/man_idle.png').convert()

    while 1:

        if not running:
            print('not running')
            break

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu.set_active(1)
                elif event.key == pygame.K_UP:
                    menu.set_active(-1)
                elif event.key == pygame.K_SPACE:
                    if menu.get_active() == len(menu.menu_items)-1:
                        running = False
                        break
                    menu.execute_action()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            offset_y += 1
            print(offset_y)

        # Make stuff after the screen.fill call
        screen.fill((0, 0, 0))

        screen.blit(image, (0, 300))
        menu.render()

        pygame.display.update()
        pygame.display.flip()