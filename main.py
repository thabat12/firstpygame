import sys, pygame
import numpy as np
import math

from map_generator.MapMaker import to_tsv, from_tsv

pygame.init()
clock = pygame.time.Clock()
size = 960, 540
screen = pygame.display.set_mode(size)

numpy_map_data = np.array([[0 for _ in range(32)] for _ in range(18)])

# so i will make 2 dictionaries and then bring it down to the right one
'''
    this will create a square grid that is compatible ONLY with 16:9 aspect ratio
    
    TODO: cleanup
    
    save level will be implemented now
'''
boxDims = size[0] // 32
xGrids, yGrids = {xPix: i for i, xPix in enumerate(range(0, size[0], size[0] // 32))}, \
                 {yPix: i for i, yPix in enumerate(range(0, size[1], size[1] // 18))}

mapMatrix = set()

active_selection, active = ['reset', 'save', 'load'], 0


def draw_grid_box(mousex, mousey, boxDims, screen):
    pygame.draw.line(screen, (255, 255, 255), (mousex // boxDims * boxDims, mousey // boxDims * boxDims),
                     (mousex // boxDims * boxDims + boxDims, mousey // boxDims * boxDims), 5)
    pygame.draw.line(screen, (255, 255, 255), (mousex // boxDims * boxDims, mousey // boxDims * boxDims),
                     (mousex // boxDims * boxDims, mousey // boxDims * boxDims + boxDims), 5)
    pygame.draw.line(screen, (255, 255, 255), (mousex // boxDims * boxDims + boxDims, mousey // 30 * boxDims),
                     (mousex // boxDims * boxDims + boxDims, mousey // boxDims * boxDims + boxDims), 5)
    pygame.draw.line(screen, (255, 255, 255), (mousex // boxDims * boxDims, mousey // boxDims * boxDims + boxDims),
                     (mousex // boxDims * boxDims + boxDims, mousey // boxDims * boxDims + boxDims), 5)


def predraw(screen_placeholder, boxDims, visited):
    for x, y in visited:
        draw_grid_box(x * boxDims, y * boxDims, boxDims, screen_placeholder)


def draw_menu(screen_p, active_selection_l, active_p, margins, default_top_offset=10):
    selected_color, unselected_color = (0, 255, 0), (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', 32)

    for ind, active_text in enumerate(active_selection_l):
        text = font.render(active_text, True, selected_color if ind == active_p else unselected_color)
        text_rect = text.get_rect()
        text_rect.center = (
            screen.get_size()[0] - text_rect.size[0] // 2 - margins,
            default_top_offset + text_rect.size[1] * ind + margins)
        screen.blit(text, text_rect)


# TODO: make new screen
def convert_matrix(coords):
    numpy_map_data.fill(0)
    for x, y in coords:
        numpy_map_data[y][x] = 1

    print(numpy_map_data)

    to_tsv(numpy_map_data, 'testing.tsv')


while 1:
    clock.tick(144)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                active = active + 1 if active + 1 < len(active_selection) else 0
            elif event.key == pygame.K_UP:
                active = active - 1 if active > 0 else len(active_selection) - 1
            elif event.key == pygame.K_SPACE:
                if active == 0:
                    mapMatrix = set()
                elif active == 1:
                    convert_matrix(mapMatrix)
                elif active == 2:
                    from_tsv('testing.tsv')

        mousex, mousey = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # saved state stuff
        screen.fill((0, 0, 0))
        draw_menu(screen, active_selection, active, 10)
        predraw(screen, 30, mapMatrix)

        # drawing the current grid
        draw_grid_box(mousex, mousey, boxDims, screen)

        # key event stuff

        if click[0]:
            mapMatrix.add((xGrids[mousex // boxDims * boxDims], yGrids[mousey // boxDims * boxDims]))
        if click[2]:
            if (xGrids[mousex // boxDims * boxDims], yGrids[mousey // boxDims * boxDims]) in mapMatrix:
                mapMatrix.remove((xGrids[mousex // boxDims * boxDims], yGrids[mousey // boxDims * boxDims]))

    pygame.display.flip()
