import pygame

'''
    Basic Menu Bar will return rectangles that are able to be rendered
    User must render the menu items manually
'''


class BasicMenuBar:
    def __init__(self, screen, menu_width, menu_height, center=True, margin_left=0,
                 margin_top=0, font_size=30, menu_items=['test'], menu_actions=[],
                 background_color=(255, 255, 255), menu_items_color=(255, 255, 255), font_color=(0, 0, 0),
                 active_color=(0, 255, 0), menu_title='Menu', ignore_title=False, spacing= 0.1):
        if not menu_items or not menu_actions or len(menu_items) != len(menu_actions):
            raise Exception('''
                Menu items and actions are not paried properly
                - must be at least one menu item
                - menu items must correspond with menu actions
            ''')

        self.screen = screen
        screen_size = screen.get_size()
        print(f'screen size {screen_size}')

        if center:
            self.pos_left, self.pos_top = (screen_size[0] // 2) - (menu_width // 2), (screen_size[1] // 2) - (
                        menu_height // 2)
            self.menu_bar = pygame.rect.Rect(self.pos_left, self.pos_top, menu_width, menu_height)
        else:
            self.pos_left, self.pos_top = margin_left, margin_top
            self.menu_bar = pygame.rect.Rect(self.pos_left, self.pos_top, menu_width, menu_height)

        # assigning all constants
        self.menu_items = menu_items
        self.menu_actions = menu_actions
        self.font_size = font_size
        self.menu_background_color = background_color
        self.menu_items_color = menu_items_color
        self.font_color = font_color
        self.active_color = active_color
        self.menu_title = menu_title
        self.ignore_title = ignore_title
        self.spacing = spacing

        self.active = 0

        print(self.menu_items)

    def render(self):
        menu_items_list = self.get_menu_items_list()
        pygame.draw.rect(self.screen, self.menu_background_color, self.menu_bar)

        self.screen.blit(menu_items_list[0][0], menu_items_list[0][1])

        for text, text_rect in menu_items_list[1:]:
            # TODO: make fancy menu tiles
            # menu_tile = pygame.rect.Rect(text_rect.left, text_rect.top, text_rect.width, text_rect.height)
            # pygame.draw.rect(self.screen, self.menu_items_color, menu_tile)
            # print(f'this is the text rect: {text_rect} and the pos top {self.pos_top}')
            self.screen.blit(text, text_rect)

    def get_menu_items_list(self):
        # with 90% width for space take-up
        menu_item_left_bound = self.pos_left + self.menu_bar.size[0] // 2
        menu_item_top_bound = self.pos_top + int(self.menu_bar.size[1] * 0.2)

        temp_top, temp_left = menu_item_top_bound, menu_item_left_bound

        menu_items_list = []

        font = pygame.font.Font('freesansbold.ttf', self.font_size)

        '''
            General process on how the menu items are being built
                we make the text
                center it in the right place
                add it to the render list
                set new offset for next element
        '''

        if not self.ignore_title:
            text = font.render(self.menu_title, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (
                temp_left,
                temp_top
            )

            menu_items_list.append((text, text_rect))
            temp_top += int(text.get_size()[1]*self.spacing)

        for ind, menu_item in enumerate(self.menu_items):
            if ind == self.active:
                text = font.render(menu_item, True, self.active_color)
            else:
                text = font.render(menu_item, True, self.font_color)

            text_rect = text.get_rect()
            text_rect.center = (
                menu_item_left_bound,
                temp_top
            )

            temp_top += int(text.get_size()[1]*self.spacing)

            menu_items_list.append((text, text_rect))

        return menu_items_list

    def set_active(self, where=0):
        if where == 0:
            raise Exception('Must provide the named argument, where= greater than or less than zero')
        if where > 0:
            self.active = self.active + 1 if self.active < len(self.menu_items)-1 else 0
        else:
            self.active = self.active - 1 if self.active > 0 else len(self.menu_items) - 1

    def execute_action(self, *args, **kwargs):
        action = self.menu_actions[self.active]
        action(*args, **kwargs)

    def get_active(self):
        return self.active
