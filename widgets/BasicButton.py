import pygame
from internal.PygameApp import Graphic

'''
    Buttons for clicking things around the screen
        - text
        - images
        - actions supplied
        - borders, active colors, image resizing!
        - supports toggle mode and button clicking mode
'''


class BasicButton:
    def __init__(self, dims, pos, screen, action, background_color=(255, 255, 255),
                 active_color=(255, 0, 0), text=None, font_size=15, font_style='freesansbold.ttf',
                 font_color=(0, 0, 0), src=None, graphic=None, border=None, padding=10, active_border_color=(255, 0, 0),
                 border_color=(0, 0, 0), image_dims=None, cursor=False, toggle=False, *args, **kwargs):

        if not callable(action):
            raise Exception('''
                Provided action must be of type function
            ''')

        # constants for rendering
        img_dims = (min(dims) - (padding << 1), min(dims) - (padding << 1))
        if image_dims:
            img_dims = image_dims

        if src:
            self.btn_image = Graphic(src, img_dims, screen)
        elif graphic:
            self.btn_image = graphic
        else:
            self.btn_image = None

        self.button_obj = pygame.rect.Rect(pos, dims)
        self.background_color = background_color
        self.active_color = active_color
        self.text = text
        self.border = border
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.cursor = cursor
        self.toggle = toggle

        # either through ratios or pixel values
        self.width = dims[0] if dims[0] > 1 else screen.width * dims[0]
        self.height = dims[1] if dims[1] > 1 else screen.heigth * dims[1]
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.padding = padding

        # font stuff
        self.font = pygame.font.Font(font_style, font_size)
        self.title_text = self.font.render(text, True, font_color)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (
            self.pos_x + (self.width >> 1),
            self.pos_y + (self.height >> 1)
        )

        self._active = False
        self._screen = screen
        self._pressed = False

        self.__action = action

    def render(self):
        # if there is a cursor, button will automatically handle active state
        # otherwise, user must do that by themselves
        self.__set_active()

        if self.toggle:
            self._active = self._pressed if self._pressed else self._active

        pygame.draw.rect(self._screen, self.background_color if not self._active else self.active_color,
                         self.button_obj)

        if self.border:
            pygame.draw.rect(self._screen,
                             self.active_border_color if self._active else self.border_color, self.button_obj,
                             self.border)

        if self.btn_image:
            self.btn_image.render((self.pos_x + self.padding, self.pos_y + self.padding))

        if self.text:
            self._screen.blit(self.title_text, self.title_rect)

    def __is_cursor_hover(self):
        x, y = pygame.mouse.get_pos()

        return abs(x - (self.pos_x + (self.width >> 1))) < (self.width >> 1) and abs(
            y - (self.pos_y + (self.height >> 1))) < (self.height >> 1)

    # cursor native behavior
    def __set_active(self):
        self._active = self.__is_cursor_hover()

    def toggle_active_with_cursor(self):
        if not self.toggle:
            raise Exception('''
                Toggle mode must be turned on!
                    ex. BasicButton( ..., toggle= True)
            ''')
        if self.__is_cursor_hover():
            self._pressed = (not self._pressed)

    def clear_toggle(self):
        if not self.toggle:
            raise Exception('''
                Toggle mode must be turned on!
                    ex. BasicButton( ..., toggle= True)
            ''')
        self._pressed = False

    # because there is only one action, we can pass *args, **kwargs
    def execute_action(self, *args, **kwargs):
        # this will be determined by the last frame call (which is close enough)
        if not self._active:
            return
        return self.__action(*args, **kwargs)


# TODO: is this the best way to solve the kwargs issues in python?
class BasicButtonGalleryOptions(BasicButton):
    def __init__(self, *args, **kwargs):
        # make a basic button but add some properties to use specifically for gallery options
        button_page_index = None
        for kwarg in kwargs:
            if kwarg == 'button_page_index':
                button_page_index = kwargs[kwarg]

        if button_page_index is None:
            raise Exception(f'''
                No button_page_index parameter supplied (are you sure you meant to use this class?)
                    supply this parameter to use the class
                    
                    ex. BasicButtonGalleryOptions( ..., button_page_index= <integer-variable>)
            ''')

        super().__init__(*args, **kwargs)

        self.__button_page_index = button_page_index

    def get_button_page_index(self):
        return self.__button_page_index

    def get_is_active(self):
        return self._active

    # overriding function to avoid redundant cursor hover check (specific case for gallery button)
    def toggle_active_with_cursor(self):
        self._pressed = (not self._pressed)
