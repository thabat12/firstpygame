import os
import pygame
import math

from internal.PygameApp import Graphic, order_files_by_index
from .BasicButton import BasicButtonGalleryOptions

'''
    Basic Gallery Options
        Purpose: There are a list of options that we need to select/ toggle, but the issue is that we need to render
            each one of them, and if there are a lot then we might need to possibly tab through each one. This is 
            a lot of work to remake each time so that's why this class needs to exist.
            
            
    How it works:
        1. Press any of the options that are on the gallery list
        2. Gallery list will return a tag that either corresponds to user's own tags or None
        3. Gallery list will also toggle the selection buttons when rendering 
            (depending on user preference)
        4. User uses the returned tags for whatever purpose they need
'''


# TODO: make the text description list optional later
class GalleryOptions:
    def __init__(self, tile_dims, pos, screen, image_list_src='', text_description_list=[], tag_list=[],
                 font_style='freesansbold.ttf', font_color=(0, 0, 0), gallery_background_color=(255, 255, 255),
                 padding=None, tile_horizontal_spacing=10, tile_vertical_spacing=10, font_size=20, title='',
                 title_color=(0, 0, 0), title_font_size=20, grid_dims=None, tile_border=5, cursor=True,
                 page_arrow_color=(255, 0, 0), page_arrow_size=15, page_active_color=(0, 255, 0),
                 page_arrow_border_color=None, page_arrow_border_active_color=(0, 0, 0), page_arrow_border=5,
                 is_toggle=False):

        if not tile_dims:
            tile_dims = (100, 100)

        # default grid dimensions are 3x2
        if not grid_dims:
            grid_dims = (3, 2)

        if not image_list_src or not tag_list:
            raise Exception('''
                    There needs to be a list of tags, so you can get the results of the gallery option!
                        lmao u suck at this
                ''')

        if padding and set(padding.keys()) != {'t', 'b', 'l', 'r'}:
            raise Exception('''
                    Padding needs to only have top and bottom parameters as key values as such:
                        ex. padding = {'t':10, 'b':10, 'l':10, 'r':10} 
                        NOTE only 't', 'b', 'l', and 'r' are the keys
                ''')

        self.tile_dims = tile_dims
        self.grid_dims = grid_dims
        self.pos = pos
        self.__screen = screen
        self.tile_dims = tile_dims
        self.image_list_src = image_list_src
        self.tag_list = tag_list
        self.text_description_list = text_description_list
        self.font_color = font_color
        self.gallery_background_color = gallery_background_color
        self.padding = padding if padding else {'t': 10, 'b': 10, 'l': 10, 'r': 10}
        self.tile_horizontal_spacing = tile_horizontal_spacing
        self.tile_vertical_spacing = tile_vertical_spacing
        self.font_size = font_size
        self.font_style = font_style
        self.title = title
        self.title_color = title_color
        self.title_font_size = title_font_size
        self.tile_border = tile_border
        self.cursor = cursor
        self.page_arrow_color = page_arrow_color
        self.page_arrow_size = page_arrow_size
        self.page_active_color = page_active_color
        self.page_arrow_border_color = page_arrow_border_color
        self.page_arrow_border = page_arrow_border
        self.page_arrow_border_active_color = page_arrow_border_active_color
        self.is_toggle = is_toggle

        # title object (doing this first for height calculation)
        self.title_font = pygame.font.Font(self.font_style, self.title_font_size)
        self.font = pygame.font.Font(self.font_style, self.font_size)

        # sample text to see what size its going to be
        sample_font = self.font.render('sample', True, (0, 0, 0))
        sample_font_height = sample_font.get_height() if text_description_list else 0

        # title may or may not take up space when rendering
        self.title_to_render = self.title_font.render(self.title, True, self.title_color)
        self.title_to_render_rect = self.title_to_render.get_rect()

        # toggle buttons may or may not be present
        self.are_page_arrows = len(self.tag_list) // (self.grid_dims[0] * self.grid_dims[1]) != 0
        page_arrow_w = (self.page_arrow_size + self.tile_horizontal_spacing) if self.are_page_arrows else 0

        # calculating width and height for the pane box dimensions
        self.width = (self.tile_dims[0] * self.grid_dims[0]) + self.padding['l'] + self.padding['r'] + \
                     (self.tile_horizontal_spacing * (self.grid_dims[0] - 1)) + page_arrow_w * 2
        self.height = (self.tile_dims[1] * self.grid_dims[1]) + self.padding['t'] + self.padding['b'] + \
                      (self.tile_vertical_spacing * (self.grid_dims[1] - 1)) + self.title_to_render.get_size()[1] + \
                      (self.grid_dims[1] * sample_font_height)

        self.title_to_render_rect.center = (
            self.pos[0] + (int(self.width) >> 1),
            self.pos[1] + self.padding['t'] + (self.title_to_render.get_size()[1] >> 2)
        )

        self.render_start_y_offset = self.title_to_render_rect.center[1] + (self.title_to_render.get_size()[1] >> 2)

        # pane box object
        self.pane_background_obj = pygame.rect.Rect(pos, (self.width, self.height))

        '''
            now for the images... generating based on the tile selection things
                these are just going to be buttons but there needs to be some toggle options
                also for toggles, this thing has to make sure its pressing the right thing
                
                confusing 
        '''
        # index corresponds to tag
        self.tag_map = {i: tag for i, tag in enumerate(self.tag_list)}

        self.image_list = []
        self.button_list = []

        # this is going to be used for the rendering/ indexing
        self.page_list = []
        self.active_page = 0

        # this thing will be switched off/on depending on the situation
        self.current_toggle = None

        self.__init_tile_tabs()

    def __init_tile_tabs(self):

        # first i need to load the images for the buttons
        image_files = os.listdir(self.image_list_src)
        image_files_list = []
        # TODO: order the image files by number index, seems like i could use a module for this

        # we will have an image list
        for img_file in image_files:
            cur_file = os.path.join(self.image_list_src, img_file)
            image_files_list.append(cur_file)

        if not (len(image_files_list) == len(self.tag_list)):
            raise Exception(f'''
                The length of the image list does not correspond to the tag list (things will get buggy!)
                    image list: {self.image_list}
                    tag list: {self.tag_list}
            ''')

        # ordering the image files list
        image_files_list = order_files_by_index(image_files_list)

        # all the total tiles divided by how many each page can hold (ceil the result)
        # also going to figure out the spacing here for each page
        page_pos_list = []
        x_pos_w_page_arrow = self.page_arrow_size if self.are_page_arrows else 0
        xpos, ypos = self.padding['l'] + self.page_arrow_size + self.tile_horizontal_spacing, self.padding[
            't'] + self.render_start_y_offset
        for r in range(self.grid_dims[1]):
            for c in range(self.grid_dims[0]):
                page_pos_list.append((xpos, ypos))
                xpos += self.tile_dims[0] + self.tile_horizontal_spacing

            ypos += self.tile_dims[1] + self.tile_vertical_spacing
            xpos = self.padding['l'] + self.page_arrow_size + self.tile_horizontal_spacing

        # filling the page list with the proper spacing for each page
        # for every batch of n elements in each grid, assign positions on the page
        filled = False
        for i in range(0, len(self.tag_list), self.grid_dims[0] * self.grid_dims[1]):
            cur_page = []

            if filled:
                break

            for j in range(0, self.grid_dims[0] * self.grid_dims[1]):
                # if there is nothing left to append to page, break out
                if len(self.tag_list) == i + j:
                    filled = True
                    break

                cur_btn = BasicButtonGalleryOptions(
                    self.tile_dims, page_pos_list[j], self.__screen, lambda x: self.tag_map[x], toggle=self.is_toggle,
                    border=self.tile_border, src=image_files_list[i + j], padding=self.tile_border,
                    button_page_index=i + j
                )

                cur_text_to_append = None
                if self.text_description_list:
                    cur_text = self.font.render(self.text_description_list[i + j], True, self.font_color)
                    cur_text_rect = cur_text.get_rect()
                    cur_text_rect.center = (
                        cur_btn.pos_x + (self.tile_dims[0] >> 1),
                        cur_btn.pos_y + self.tile_dims[1] + (self.tile_vertical_spacing >> 1)
                    )

                    cur_text_to_append = (cur_text, cur_text_rect)

                cur_page.append((cur_btn, cur_text_to_append))

            self.page_list.append(cur_page)

        # finally (before i lose my mind and become insane), time to make the arrows render
        self.left_arrow_points, self.right_arrow_points = None, None
        self.left_arrow_hit_box, self.right_arrow_hit_box = None, None

        if self.are_page_arrows:
            self.left_arrow_points = (
                (self.pos[0] + self.padding['l'] + self.page_arrow_size,
                 self.pos[1] + (self.height >> 1) - (self.page_arrow_size >> 1)),
                (self.pos[0] + self.padding['l'], self.pos[1] + (self.height >> 1)),
                (self.pos[0] + self.padding['l'] + self.page_arrow_size,
                 self.pos[1] + (self.height >> 1) + (self.page_arrow_size >> 1))
            )

            self.right_arrow_points = (
                (self.pos[0] + self.width - self.padding['r'] - self.page_arrow_size,
                 self.pos[1] + (self.height >> 1) - (self.page_arrow_size >> 1)),
                (self.pos[0] + self.width - self.padding['r'], self.pos[1] + (self.height >> 1)),
                (self.pos[0] + self.width - self.padding['r'] - self.page_arrow_size,
                 self.pos[1] + (self.height >> 1) + (self.page_arrow_size >> 1))
            )

            # for future reference to detect clicking, making
            # format : ( (x1, y1), (x2, y2) )
            self.left_arrow_hit_box = (
                (self.left_arrow_points[1][0], self.left_arrow_points[0][1]),
                (self.left_arrow_points[2][0], self.left_arrow_points[2][1])
            )

            self.right_arrow_hit_box = (
                (self.right_arrow_points[0][0], self.right_arrow_points[0][1]),
                (self.right_arrow_points[1][0], self.right_arrow_points[2][1])
            )

    def render(self):
        pygame.draw.rect(self.__screen, self.gallery_background_color, self.pane_background_obj)
        self.__screen.blit(self.title_to_render, self.title_to_render_rect)

        page = self.page_list[self.active_page]

        for btn, text in page:
            btn.render()
            if self.text_description_list:
                self.__screen.blit(text[0], text[1])

        if self.are_page_arrows:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # TODO: get the points and store them to avoid recomputation
            left_active, right_active = self.__is_mouse_pos_in_left_arrow_hit_box(mouse_x, mouse_y), \
                                            self.__is_mouse_pos_in_right_arrow_hit_box(mouse_x, mouse_y)

            pygame.draw.polygon(self.__screen, self.page_arrow_color if not left_active else self.page_active_color, self.left_arrow_points)
            pygame.draw.polygon(self.__screen, self.page_arrow_color if not right_active else self.page_active_color, self.right_arrow_points)

            if self.page_arrow_border_color:
                pygame.draw.polygon(self.__screen, self.page_arrow_border_color if not left_active else self.page_arrow_border_active_color,
                                    self.left_arrow_points, self.page_arrow_border)
                pygame.draw.polygon(self.__screen, self.page_arrow_border_color if not right_active else self.page_arrow_border_active_color,
                                    self.right_arrow_points, self.page_arrow_border)

    # query every button until one is (maybe) found... query page buttons until one is (maybe) found
    def click_action_with_cursor(self):
        if not self.cursor:
            raise Exception('''
                Warning: cursor is disabled
                    you have to enable cursor to be able to use this method or things will get buggy
                    
                    ex. BasicGalleryOptions( ... cursor=True)
            ''')

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # storing the active page as a list of buttons that the current page is showing (this is used later in function)
        active_page = self.page_list[self.active_page]

        # if the mouse clicks are out of the boundary, return early (save computation time)
        if (mouse_x > self.pos[0] + self.width) or (mouse_x < self.pos[0]) or \
                (mouse_y < self.pos[1]) or (mouse_y > self.pos[1] + self.height):
            return None

        # if x and y are within the box constraints of the page buttons, then page forward or backwards
        if self.__is_mouse_pos_in_left_arrow_hit_box(mouse_x, mouse_y):
            self.active_page = len(self.page_list)-1 if (self.active_page == 0) else self.active_page - 1
            return None
        elif self.__is_mouse_pos_in_right_arrow_hit_box(mouse_x, mouse_y):
            self.active_page = 0 if (self.active_page == len(self.page_list) - 1) else self.active_page + 1
            return None

        # querying each button to see whether user is on one and will return the tag result -- O(N) complexity
        for btn, _ in active_page:
            ind = btn.get_button_page_index()
            res = btn.execute_action(ind)

            # buttons can return tags, if the tag is returned (from lambdas), then return and break out
            if res is not None:
                btn.toggle_active_with_cursor()
                if self.current_toggle:
                    self.current_toggle.clear_toggle()

                self.current_toggle = btn

                return res

    # formatted like this: ((x1, y1), (x2, y2))
    def __is_mouse_pos_in_left_arrow_hit_box(self, mouse_x, mouse_y):
        return self.left_arrow_hit_box[0][0] <= mouse_x <= self.left_arrow_hit_box[1][0] and \
                    self.left_arrow_hit_box[0][1] <= mouse_y <= self.left_arrow_hit_box[1][1]

    def __is_mouse_pos_in_right_arrow_hit_box(self, mouse_x, mouse_y):
        return self.right_arrow_hit_box[0][0] <= mouse_x <= self.right_arrow_hit_box[1][0] and \
                self.right_arrow_hit_box[0][1] <= mouse_y <= self.right_arrow_hit_box[1][1]

    def page_forward(self):
        self.active_page = 0 if (self.active_page == len(self.page_list) - 1) else self.active_page + 1

    def page_backward(self):
        self.active_page = len(self.page_list)-1 if (self.active_page == 0) else self.active_page - 1
