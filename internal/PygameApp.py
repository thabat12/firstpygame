import abc
import functools, os
import pygame
from abc import ABC, abstractmethod

'''
    @PygameApp:
        Creates the window and initializes everything for you
        Supports function based windows that can be added on to each other
'''


class PygameApp:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

        # what keyword arguments are supported
        self.acceptable_kwargs = {
            'size'
        }

    def __call__(self, *args, **kwargs):
        for kwarg, val in kwargs.items():
            if kwarg == 'size':
                pygame.display.set_mode(val)
            if kwarg == 'screen':
                self.screen = val
        pygame.init()

        return self.func(*args, **kwargs)


'''
    @Screen:
            Verifies that the function parameters are set correctly
            Validates the new function-based screen
'''


class Screen:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        print(args, kwargs)
        if len(args) != 2 and len(kwargs) != 2:
            raise Exception('''
                There should be 2 arguments
                    1. size (as tuple)
                    2. screen (pygame Surface object)
            ''')

        for arg in args:
            if isinstance(arg, pygame.Surface) or isinstance(arg, tuple):
                continue
            else:
                raise Exception(f'''
                    Invalid argument type: {type(arg)}
                ''')

        return self.func(*args, **kwargs)


'''
    RenderTileMap *tries* to be efficient by:
        - converting the supplied tile map into pre-rendered sections on the screen
        - scrolling around the background as the camera "moves"
    
    Problems to solve:
        - dynamic components, like animations
        - enemy character models (load or not load?)


'''


# TODO: implements render tile map
class RenderTileMap:
    pass


'''
    Loading images with pygame in easier ways
        - hold list of graphics 
        - update and display each one of them
'''


class Graphic:
    def __init__(self, src, dims, screen):
        if not os.path.isfile(src):
            raise Exception(f'''
                Supplied file does not exist:
                    {src}
            ''')

        self.image = pygame.image.load(src).convert_alpha()
        self.image = pygame.transform.scale(self.image, dims)
        self.__screen = screen

    def render(self, pos):
        self.__screen.blit(self.image, pos)


class Animation(ABC):
    def __init__(self, src_folder, dims, screen, fps=60):

        if not os.path.isdir(src_folder):
            raise Exception('''
                No such directory present
            ''')

        self.sprites = []

        for filename in os.listdir(src_folder):
            self.sprites.append(Graphic(os.path.join(src_folder, filename), dims, screen))

        self.clock = 0
