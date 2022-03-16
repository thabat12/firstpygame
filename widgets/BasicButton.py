import pygame
from internal.PygameApp import Graphic

'''
    Buttons for clicking things around the screen
        - text
        - images
        - actions supplied
        - borders, active colors, image resizing!
'''


class BasicButton:
    def __init__(self, dims, pos, action, screen, background_color=(255, 255, 255),
                 active_color=(255, 0, 0), text=None, font_size=15, font_style='freesansbold.ttf',
                 font_color=(0,0,0), src=None, border=None, padding=10, active_border_color=(255, 0, 0),
                 border_color = (0, 0, 0), image_dims=None):

        if not callable(action):
            raise Exception('''
                Provided action must be of type function
            ''')

        # constants for rendering
        img_dims = (min(dims) - (padding << 1), min(dims) - (padding << 1))
        if image_dims:
            img_dims = image_dims

        self.btn_image = Graphic(src, img_dims, screen) if src else None
        self.button_obj = pygame.rect.Rect(pos, dims)
        self.background_color = background_color
        self.active_color = active_color
        self.text = text
        self.border = border
        self.border_color = border_color
        self.active_border_color = active_border_color

        # either through ratios or pixel values
        self.width = dims[0] if dims[0] >= 1 else screen.width * dims[0]
        self.height = dims[1] if dims[1] >= 1 else screen.heigth * dims[1]
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

        self.__active = False
        self.__screen = screen

        self.__action = action

    def render(self):
        self.__get_active()
        pygame.draw.rect(self.__screen, self.background_color if not self.__active else self.active_color,
                         self.button_obj)

        if self.border:
            pygame.draw.rect(self.__screen,
                             self.active_border_color if self.__active else self.border_color, self.button_obj, self.border)

        if self.btn_image:
            self.btn_image.render((self.pos_x + self.padding, self.pos_y + self.padding))

        if self.text:
            self.__screen.blit(self.title_text, self.title_rect)

    def __get_active(self):
        x, y = pygame.mouse.get_pos()

        if abs(x - (self.pos_x + (self.width >> 1))) < (self.width >> 1) and abs(y - (self.pos_y + (self.height >> 1))) < (self.height >> 1):
            self.__active = True
        else:
            self.__active = False

    # because there is only one action, we can pass *args, **kwargs
    def execute_action(self, *args, **kwargs):
        if not self.__active:
            return

        return self.__action(*args, **kwargs)
