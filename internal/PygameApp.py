import functools
import pygame
import time

'''
    Makes shit organized
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


class RenderTileMap:
    pass
