import sys, os
import pygame

sys.path.append(os.getcwd())

from screens.HomeScreen import main_screen

size = (1080, 540)
screen = pygame.display.set_mode(size)


print('cur dir is ' + os.getcwd())
main_screen(sizep=size, screenp=screen)