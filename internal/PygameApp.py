import abc
import functools, os, warnings
import pygame
import time
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
    A common problem that I'm running into, ordering files based on index values, 
    so now its time to make a simple function to handle that... this file is being placed
    here because that's just how the order requires it... im still kind of a noob but i think
    theres no other way to make it more "global" other than to make my own module but this file
    itself is a module that's good enough
'''


def order_files_by_index(file_list):
    def convert_digits(digits):
        res = 0

        for d in digits:
            res *= 10
            res += d

        return res

    def get_file_index(file):
        start = None

        if file[0].isdigit():
            start = 0
        elif '.' in file:
            # have to files ending with things like ".png" validated too
            rev_ind = file.rindex('.')
            if not file[rev_ind - 1].isdigit():
                raise Exception(f'''
                                Invalid file ordering! 
                                    - file order must be given index either strictly at the end of the file name
                                        or at the beginning 

                                    error file: {file}
                            ''')
            else:
                start = rev_ind - 1

        cur = start
        digits = []

        while file[cur].isdigit():
            digits.append(int(file[cur]))
            cur = cur + 1 if (start == 0) else cur - 1

        return convert_digits(digits)

    return sorted(file_list, key=lambda x: get_file_index(x))


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
        - update and display
        - load images easily
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
        self.__src = src
        self.__screen = screen

    def render(self, pos):
        self.__screen.blit(self.image, pos)

    def __str__(self):
        return f'Image at {self.__src}'


'''
    Animations will be cyclical ListNodes (its just easier)
'''


class ListNode:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        res = []

        head = self
        cur = self
        res.append(f'({cur.val})')
        cur = cur.next

        while cur and (cur is not head):
            res.append(f' -> ({cur.val})')
            cur = cur.next

        return ''.join(res)


'''
    Animation is very chunky but here are the main functions
        __next__
            get the next frame --- will calculate time elapsed and everything for proper frame rates
        reset()
            go to default frame for next call
            
        internally, animation is a cyclical linked list, and it will keep calling next over and over
        again for the next frames, pretty simple
'''


class AnimationSequence:
    def __init__(self, dims, screen, delay_seconds=1, animation_sequence=None, src_folder=''):

        using_path, using_sequence = os.path.isdir(src_folder), bool(animation_sequence)
        print(using_path, using_sequence)

        if using_path == using_sequence:
            raise Exception('''
                Must provide either src folder containing list of animation sequences
                    ex. animation_sequence= [Graphics(...), Graphics(...), ...]
                        OR
                    ex. src_folder= '<dir>/<dir_containing_animations>
                        inside of <dir_containing_animations>...
                            
                            -dir containing animations (NOTE: must provide animation indexing)
                                - <animationname>0.png
                                - <animationname>1.png
                                
                    MUST BE ONE OR THE OTHER (you can't provide both parameters because thats confusing)
            ''')

        self.head = ListNode()
        self.cur = self.head
        self.__frame_len = 0

        # first get all image refs
        if using_path:
            self.__init_with_filepath(src_folder=src_folder, dims=dims, screen=screen)
        elif using_sequence:
            self.__init_with_sequence(animation_sequence=animation_sequence, dims=dims, screen=screen)

        self.delay_seconds = delay_seconds
        self.elapsed = 0
        self.start = 0

    def __init_with_filepath(self, src_folder, dims, screen):
        files = os.listdir(src_folder)

        # try to order the files, but if that doesn't work, don't bother
        try:
            files = order_files_by_index(files)
        except:
            warnings.warn(f'''
                Filenames are not properly indexed in src folder: {src_folder}
                    proper file names for animations must have a numberical index
                    order either strictly at the beginning or end of the file name
                    
                    ex. <filename>0.png OR 0<filename>.png
            ''')
            print('')

        # starting the process
        self.cur.val = Graphic(os.path.join(src_folder, files[0]), dims, screen)
        self.__frame_len += 1

        for file in files[1:]:
            cur_file = os.path.join(src_folder, file)
            if not os.path.isfile(cur_file):
                raise Exception('''
                                Something is not a file
                                    make sure there are no directories and other things supplied because
                                    this program is going to write some extra files and expects a specific
                                    structure.
                            ''')

            self.cur.next = ListNode(Graphic(cur_file, dims, screen))
            self.cur = self.cur.next

            self.__frame_len += 1

        # connecting the tail to the head
        self.cur.next = self.head
        self.cur = self.head

    def __init_with_sequence(self, animation_sequence, dims, screen):
        # since these are already graphic type object, no need to cast them into graphics
        self.cur.val = animation_sequence[0]

        for sequence in animation_sequence[1:]:
            self.cur.next = ListNode(sequence)
            self.cur = self.cur.next

        # connecting the tail to the head
        self.cur.next = self.head
        self.cur = self.head

        self.__frame_len = len(animation_sequence)

    # reset animation sequence
    def reset(self):
        self.cur = self.head

    # works like an iterator
    def __iter__(self):
        return self.cur

    # works with time delays
    def __next__(self):
        self.elapsed = time.time()

        if self.elapsed - self.start > self.delay_seconds:
            self.cur = self.cur.next
            self.start = time.time()

        return self.cur

    def __len__(self):
        return self.__frame_len
