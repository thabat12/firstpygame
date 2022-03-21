import sys, os
from abc import ABC, abstractmethod, abstractproperty
import pygame

from internal.PygameApp import Graphic

'''
    BasicWidget (ABSTRACT) is the parent of all widget classes and requires the common functionality to render
        - every widget requires pos, dims, and screen argument
        - the class also defines the background object box (to be blit onto screen on render)
        
        Special cases:
            - padding GROWS outwards** adding padding values implicitly increases the dimensions of widget
            - if dim ratios are <= 1, then they will be calculated as a portion value of the screen
'''


# TODO: exception handling for improper arguments
class BasicWidget(ABC):
    def __init__(self, pos, dims, screen, background_color=(255, 255, 255), title='', title_size=15,
                 font_style='freesansbold.ttf', title_color=(0, 0, 0), border=0, border_color=(0, 0, 0),
                 padding=None, **kwargs):
        # position coordinates are centered
        self._pos = pos
        # this value may change again due to padding
        self._dims = (dims[0] if dims[0] > 1 else int(screen.get_size()[0] * dims[0]),
                      dims[1] if dims[1] > 1 else int(screen.get_size()[1] * dims[1]))
        self._screen = screen
        self._background_color = background_color
        self._title = title
        self._title_size = title_size
        self._font_style = font_style
        self._title_color = title_color
        self._border = border
        self._border_color = border_color
        self._padding = {'t': 0, 'b': 0, 'l': 0, 'r': 0} if not padding else padding
        # padding GROWS outwards*
        self._dims = (self._dims[0] + self._padding['l'] + self._padding['r'],
                      self._dims[1] + self._padding['t'] + self._padding['b'])

        # background object box
        s = pygame.Surface(self._dims, pygame.SRCALPHA)
        s.fill(self._background_color)
        self._background_object_box = s

        # for blit method inside render, saving render x and render y coordinates, avoids re-computation
        self._render_x_pos, self._render_y_pos = self._pos[0] - (self._dims[0] >> 1), self._pos[1] - (
                    self._dims[1] >> 1)
        # title is also in this category, but will leave to concrete classes to position title in render
        title_font = pygame.font.Font(self._font_style, self._title_size)
        self._title_font_to_render = title_font.render(self._title, True, self._title_color)
        self._title_font_to_render_rect = self._title_font_to_render.get_rect()

    # check if mouse is over the current widget (useful for clickable queries)
    def is_cursor_hover(self, x=None, y=None):
        if not x and not y:
            x, y = pygame.mouse.get_pos()

        return (self._pos[0] - (self._dims[0] >> 1)) <= x <= (self._pos[0] + (self._dims[0] >> 1)) and \
               (self._pos[1] - (self._dims[1] >> 1)) <= y <= (self._pos[1] + (self._dims[1] >> 1))

    # render orders and logic vary for each type of component, but every widget must support rendering
    @abstractmethod
    def render(self):
        pass


'''
    BasicWidgetClickable (ABSTRACT) supports clickable widgets that come with actions
        - actions can be user defined functions or may return tags to manipulate later on
        - since there is now an active state, active color states are also "unlocked"
        - this class handles everything about states:
            - is_pressed
            - is_active
        - supports cursor but user can also manually manipulate states (it will be more complicated though)
        - toggle feature (locks active/ inactive state)
'''


# TODO: exception handling for improper arguments
class BasicWidgetClickable(BasicWidget):
    def __init__(self, action=lambda: None, active_color=(255, 255, 255), active_border_color=(0, 0, 0),
                 active_font_color=(0, 0, 0), cursor=False, toggle=False, **kwargs):
        super().__init__(**kwargs)

        self._action = action
        self._active_color = active_color
        self._active_border_color = active_border_color
        self._active_font_color = active_font_color
        self._cursor = cursor
        # this will stay "more" private to maintain consistent action
        self.__toggle = toggle

        self._active, self._pressed = False, False

        # background object box ACTIVE variant
        s = pygame.Surface(self._dims, pygame.SRCALPHA)
        s.fill(self._active_color)
        self._background_object_box_active = s

        title_font_active = pygame.font.Font(self._font_style, self._title_size)
        self._title_font_to_render_active = title_font_active.render(self._title, True, self._active_font_color)

        # border variant
        if self._border:
            self._border_rect = pygame.rect.Rect((self._render_x_pos, self._render_y_pos), self._dims)

    # by default, clickable will handle the background active stuff for you
    @abstractmethod
    def render(self):
        # first, set active variable for future use
        self.__set_active_with_cursor()

        # override active state if toggle
        if self.__toggle and self._pressed:
            self._active = True

        self._screen.blit(self._background_object_box if not self._active else self._background_object_box_active,
                          (self._render_x_pos, self._render_y_pos))

        if self._border:
            pygame.draw.rect(self._screen, self._border_color if not self._active else self._active_border_color,
                             self._border_rect, self._border)

    '''
        Functions for handling states:
            active: for hovering states or current selection
                
                set_active_with_cursor()
                    for rendering what is active
                    
                set_active_without_cursor()
                    manually setting, public method
            
            pressed: for persistent selection (in toggle mode)
            
                toggle_with_cursor()
                    if mouse is over then flip pressed state, otherwise don't do anything
                
                toggle_without_cursor()
                    flip pressed state if the current object is active
                
                clear_toggle()
                    pressed state defaults to False  
                    
            These states mainly affect rendering behavior, except action can only be called
            once the object is in the active state
    '''

    def __set_active_with_cursor(self):
        self._active = self.__is_active_hover()

    # works kind of like toggle
    def set_active_without_cursor(self):
        self._active = (not self._active)

    def toggle_with_cursor(self):
        if not self.__toggle:
            raise Exception('''
                Toggle mode must be turned on!
                    ex. BasicButton( ..., toggle= True)
            ''')
        if self.__is_active_hover():
            self._pressed = (not self._pressed)

    def toggle_without_cursor(self):
        if self._active:
            self._pressed = (not self._pressed)

    def clear_toggle(self):
        if not self.__toggle:
            raise Exception('''
            Toggle mode must be turned on!
                    ex. BasicButton( ..., toggle= True)
            ''')
        self._pressed = False

    '''
        execute_action affects game behavior by calling whatever function the user
        provides
        
        execute_action will not work if the current object is not in the active state
    
    '''

    def execute_action(self, *args, **kwargs):
        if not self._active:
            return
        return self._action(*args, **kwargs)

    # here is a blanket statement click action, for convenience when making more implementations
    def click(self, *args, **kwargs):
        if self._cursor:
            # if on cursor, query all cursor methods
            if self.__toggle:
                self.toggle_with_cursor()
                if self._pressed:
                    return self.execute_action(*args, **kwargs)
                else:
                    # if we undo the toggle, there is no need to return the tag/ function again
                    return None
            else:
                return self.execute_action(*args, **kwargs)
        else:
            # if not on cursor, just check for active
            if self._active:
                return self.execute_action(*args, **kwargs)
            else:
                return None

    # more explicit way to check if mouse is over clickable element
    def __is_active_hover(self):
        return self.is_cursor_hover()


'''
    BasicButton (CONCRETE) will support further design features and is based on the 
        BasicWidgetClickable class... 
        
        

'''


class BasicButton(BasicWidgetClickable):
    def __init__(self, pos, dims, screen, background_color=(255, 255, 255), title='', font_style='freesansbold.ttf',
                 title_color=(0, 0, 0), border=0, border_color=(0, 0, 0), padding=None, action=None,
                 active_color=(255, 255, 255), active_border_color=(0, 0, 0), active_font_color=(0, 0, 0),
                 cursor=True, toggle=False, graphic=None, src=None, image_dims=None, **kwargs):
        # explicitly passing all arguments into super
        # TODO: is there a better way to do this?
        super().__init__(pos=pos, dims=dims, screen=screen, background_color=background_color, title=title,
                         font_style=font_style, title_color=title_color, border=border, border_color=border_color,
                         padding=padding, action=action, active_color=active_color,
                         active_border_color=active_border_color, active_font_color=active_font_color, cursor=cursor,
                         toggle=toggle)

        # handling center title coords
        if self._title:
            self._title_font_to_render_rect.center = (self._pos[0], self._pos[1])

        # image dimensions made automatically to be minimum of either button dimension
        img_dims = (min(self._dims) - self._padding['l'] - self._padding['r'],
                    min(self._dims) - self._padding['t'] - self._padding['b'])
        # if image dimensions provided, then that will be defaulted value
        if image_dims:
            img_dims = image_dims

        # assigning button image to corresponding values
        if src:
            self.btn_image = Graphic(src, img_dims, screen)
        elif graphic:
            self.btn_image = graphic
        else:
            self.btn_image = None

    '''
        This render method takes into account:
            - active/ inactive states
            - if current button is pressed (applicable only to toggle mode)
    '''

    def render(self):
        super().render()

        if self.btn_image:
            self.btn_image.render((self._render_x_pos + self._padding['l'], self._render_y_pos + self._padding['t']))

        self._screen.blit(self._title_font_to_render if not self._active else self._title_font_to_render_active,
                          self._title_font_to_render_rect)


'''
    QueryGroupWidget (ABSTRACT) defines widgets made up of one or more widgets: when user clicks on this sort of 
    widget, QueryGroupWidget will essentially page through every "button" and either return the tag specified or 
        return nothing

'''


class QueryGroupWidget(BasicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._title_font_to_render_rect.center = (
            self._pos[0], self._render_y_pos + self._padding['t'] + (self._title_font_to_render.get_height() >> 1)
        )

        print(self._padding, self._title_font_to_render_rect.center[1], self._title_font_to_render.get_height(),
              'title font to render rect center y')

        self._active_page_button_list = kwargs.get('active_page_button_list')

        self._active_page = 0

    @abstractmethod
    def render(self):
        self._screen.blit(self._background_object_box, (self._render_x_pos, self._render_y_pos))
        # menu or menu groups will have a title at the top
        self._screen.blit(self._title_font_to_render, self._title_font_to_render_rect)

        for btn in self._active_page_button_list:
            btn.render()

    def change_active_page_button_list(self, new_list):
        self._active_page_button_list = new_list

    # query clicking and return tag/ function defined by the buttons
    def click(self):
        for button in self._active_page_button_list:
            res = button.click()
            if res is not None:
                return res
        return None


class BasicMenuBar(QueryGroupWidget):
    def __init__(self, pos, dims, screen, background_color=(255, 255, 255), title='', title_size=15,
                 font_style='freesansbold.ttf', title_color=(0, 0, 0), border=0, border_color=(0, 0, 0),
                 padding=None, menu_text_list=[], menu_actions=[], active_font_color=(0, 0, 0), menu_item_spacing=10,
                 title_item_spacing=0, font_size=15, font_color=(0, 0, 0), is_vertical=True, *args, **kwargs):

        if not padding:
            padding = {'t': 10, 'b': 10, 'l': 10, 'r': 10}

        text_to_render_buttons = []

        start_y_offset = padding['t'] + pos[1]

        if len(menu_text_list) % 2 != 0:
            font = pygame.font.Font(font_style, font_size)
            text_rendered = font.render('text', True, font_color)
            print('start y offset changed')
            start_y_offset = pos[1] - (text_rendered.get_height() >> 1) - (
                        (menu_item_spacing + text_rendered.get_height()) * (len(menu_text_list) // 2))

        if title_item_spacing:
            font = pygame.font.Font(font_style, title_size)
            title_rendered = font.render('title', True, font_color)
            start_y_offset = pos[1] - (dims[1] >> 1) + title_rendered.get_height() + title_item_spacing

        x_offset = pos[0]

        for ind, text in enumerate(menu_text_list):
            font = pygame.font.Font(font_style, font_size)
            text_rendered = font.render(text, True, font_color)
            text_rendered_rect = text_rendered.get_rect()
            text_rendered_rect.center = (
                x_offset, start_y_offset + (text_rendered.get_height() >> 1)
            )

            text_to_render_buttons.append(BasicButton(
                text_rendered_rect.center, text_rendered_rect.size, screen, background_color=(0, 0, 0, 0), title=text,
                font_style=font_style,
                title_color=font_color, action=menu_actions[ind], active_color=(0, 0, 0, 0),
                active_font_color=active_font_color, cursor=True
            ))

            start_y_offset += text_rendered.get_height() + menu_item_spacing

        super().__init__(pos=pos, dims=dims, screen=screen, background_color=background_color,
                         active_color=background_color, title=title, title_size=title_size,
                         font_style='freesansbold.ttf', title_color=title_color, border=border,
                         border_color=border_color,
                         padding=padding, menu_text_list=menu_text_list, menu_actions=menu_actions,
                         active_font_color=active_font_color,
                         menu_item_spacing=menu_item_spacing, font_size=font_size, font_color=font_color,
                         is_vertical=is_vertical,
                         active_page_button_list=text_to_render_buttons, *args, **kwargs)

    def render(self):
        super().render()


'''
    Basic gallery options will implement Query group widgets, meaning that there will be a gruops of
    buttons that the user is able to select
    
        functionality:
            change the current active group of buttons with pages (if there are multiple pages)
'''


class BasicGalleryOptions(QueryGroupWidget):
    def __init__(self, pos, dims, screen, background_color=(255, 255, 255), title='', title_size=15, font_size=10,
                 font_style='freesansbold.ttf', title_color=(0, 0, 0), border=0, border_color=(0, 0, 0),
                 padding=None, image_list_src='', text_description_list=[], tag_list=[], action_list=[],
                 tile_dims=(100, 100),
                 tile_horizontal_apcing=10, tile_vertical_spacing=10, page_arrow_color=(255, 0, 0), page_arrow_size=15,
                 page_active_color=(0, 255, 0),
                 page_arrow_border_color=(0, 0, 0), page_arrow_border_active_color=(0, 0, 0), page_arrow_border=0,
                 is_toggle=False, **kwargs):
        pass

    def render(self):
        pass
