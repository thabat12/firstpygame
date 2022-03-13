import pygame

from screens.HomeScreen import main_screen

size = (960, 540)
screen = pygame.display.set_mode(size)

main_screen(sizep=size, screenp=screen)