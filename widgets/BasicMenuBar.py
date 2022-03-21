import pygame


# TODO: implement tags instead of actions, update constructor to conform to other Basic classes
class BasicMenuBar:
    def __init__(self, screen, menu_width, menu_height, menu_items=[], menu_actions=[],
                 pos_x=0, pos_y=0, menu_background_color=(255, 255, 255), font_color=(0, 0, 0),
                 active_color=(0, 255, 0), title_color=(0, 0, 0), font_style='freesansbold.ttf',
                 font_size=20, title_font_size=30, menu_item_spacing=10, menu_padding=None,
                 menu_title='', cursor=False):

        """
            Handling exceptions:
                - If I am supplying a menu padding, at least have the top and bottom values
                - I need menu items that correspond to menu actions (these can be None values)
        """
        if menu_padding is None:
            menu_padding = {'t': 10, 'b': 10}
        elif set(menu_padding.keys()) != {'t', 'b'}:
            raise Exception(f'''
                Menu items MUST have top and bottom arguments as such:
                    ex. menu_padding = {{'t': 10, 'b': '10'}}

                    Supplied keys: {set(menu_padding.keys())}
            ''')

        if not menu_items or not menu_actions:
            raise Exception(f'''
                Must fill in menu_items and menu_actions with corresponding values
                    {menu_items} {'EMPTY = NOT GOOD' if not menu_items else 'OK'}
                    {menu_actions} {'EMPTY = NOT GOOD' if not menu_items else 'OK'}
                    {'Matching Length: OK' if len(menu_items) == len(menu_actions) else 'Matching Length: NOT GOOD'}
            ''')

        '''
            Setting up constants:
                - For use in later functions
                - Screen is private since I would already have that access in main code
        '''
        self.__screen = screen
        self.menu_width = menu_width if menu_width > 1 else self.__screen.get_size()[0] * menu_width
        self.menu_height = menu_height if menu_width > 1 else self.__screen.get_size()[1] * menu_height
        self.menu_items = menu_items
        self.menu_actions = menu_actions
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.menu_background_color = menu_background_color
        self.font_color = font_color
        self.active_color = active_color
        self.title_color = title_color
        self.font_style = font_style
        self.font_size = font_size
        self.title_font_size = title_font_size
        self.menu_item_spacing = menu_item_spacing
        self.menu_padding = menu_padding
        self.menu_title = menu_title
        self.cursor = cursor

        self.__active = -1 if self.cursor else 0

        '''
            The menu bar will always be the same, so no need to recalculate that every time
        '''

        # need this for rendering the actual menu
        self.menu_box_obj = pygame.rect.Rect((self.pos_x, self.pos_y), (self.menu_width, self.menu_height))
        # need this for rendering individual font texts
        self.font = pygame.font.Font(self.font_style, self.font_size)
        # this is not necessary so i'll keep it contained only here
        title_font = pygame.font.Font(self.font_style, self.title_font_size)

        # these two are the only things needed for rendering title text
        self.title = title_font.render(self.menu_title, True, self.title_color)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.pos_x + (self.menu_width // 2),
                                  self.pos_y + self.title_rect.height // 2 + self.menu_padding['t'])

        # where to start rendering the menu items, depends on the title presence
        if self.menu_title:
            self.title_rect_bottom = self.title_rect.center[1] + self.title_rect.height // 2 + self.menu_item_spacing
        else:
            self.title_rect_bottom = self.pos_y + self.menu_padding['t']

        # pre-render the menu items to avoid further computation
        # each index contains tuple of ( (menu item tile, active menu item tile), text rect )
        self.menu_items_render = []
        offset_y = self.title_rect_bottom

        for ind, menu_item in enumerate(self.menu_items):
            # get set text and text_rect based on menu item index
            text = self.font.render(menu_item, True, self.font_color)
            text_active = self.font.render(menu_item, True, self.active_color)
            text_rect = text.get_rect()
            text_rect.center = (self.pos_x + self.menu_width // 2, offset_y + text_rect.height // 2)
            offset_y += text_rect.height + self.menu_item_spacing

            self.menu_items_render.append(((text, text_active), text_rect))

    '''
        The user can implement render in whatever order he/she wants
    '''

    def render(self):
        # for now this active setting will be here
        if self.cursor:
            self.__set_active_cursor()

        pygame.draw.rect(self.__screen, self.menu_background_color, self.menu_box_obj)
        self.__screen.blit(self.title, self.title_rect)

        counter = 0
        for (text, active_text), text_rect in self.menu_items_render:
            if counter == self.__active:
                self.__screen.blit(active_text, text_rect)
            else:
                self.__screen.blit(text, text_rect)

            counter += 1

    '''
        setting active cursor can be done internally 
    '''

    # returns the index of whatever is active so far
    def is_cursor_hover(self):
        x, y = pygame.mouse.get_pos()

        for ind, menu_item in enumerate(self.menu_items_render):
            menu_item_rect = menu_item[1]

            if abs(x - menu_item_rect.center[0]) < (menu_item_rect.width >> 1) \
                    and abs(y - menu_item_rect.center[1]) < (menu_item_rect.height >> 1):
                return ind

        return -1

    def __set_active_cursor(self):
        self.__active = self.is_cursor_hover()

    # GLOBAL ACTIONS

    '''
        Active toggle is not internal behavior so user must set 
    '''

    def set_active_toggle(self, move=0):
        if move > 0:
            self.__active = self.__active + 1 if (self.__active + 1 <= len(self.menu_items) - 1) else 0
        elif move < 0:
            self.__active = self.__active - 1 if (self.__active - 1 >= 0) else len(self.menu_items) - 1

    def execute_action_toggle(self):
        if self.cursor:
            raise Exception('''
                Cursor is enabled:
                    calling the toggle function with the cursor enabled can cause errors
                    to enable the toggle to work, disable cursor in the constructor...

                    ex. BasicMenuBar( ... cursor=False)

                    note that cursor=False by default
            ''')

    def execute_action_cursor(self, btn, *args, **kwargs):
        if not self.cursor:
            raise Exception('''
                Cursor is disabled:
                    calling the cursor function with the cursor disabled can cause errors
                    to enable cursor to work, supply it in the constructor...

                    ex. BasicMenuBar( ... cursor=True)
            ''')
        # cursor actions means click events, otherwise the space bar press
        if btn == 1 and self.__active >= 0:
            return self.menu_actions[self.__active](*args, **kwargs)

    def reset_active(self):
        self.__active = -1

    def get_active(self):
        return self.__active
