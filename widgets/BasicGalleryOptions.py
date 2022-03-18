import os
import pygame

from internal.PygameApp import Graphic
from .BasicButton import BasicButton

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
        4. User uses the returned tags for whatever purpose they desire
'''

# TODO: make the text description list optional later
class BasicGalleryOptions:
    def __init__(self, tile_dims, pos, screen, image_list_src='', text_description_list=[], tag_list=[],
                 font_style='freesansbold.ttf', font_color=(0, 0, 0), gallery_background_color=(255, 255, 255),
                 padding=None, tile_horizontal_spacing=10, tile_vertical_spacing=10, font_size=20, title='',
                 title_color=(0, 0, 0), title_font_size=20, grid_dims=None):

        if not tile_dims:
            tile_dims = (100, 100)

        # default grid dimensions are 3x2
        if not grid_dims:
            grid_dims = (3, 2)

        if not image_list_src or not tag_list \
                or not (len(text_description_list) == len(tag_list)):
            raise Exception('''
                    There needs to be a list of buttons in button list of type: BasicButton that correspond to 
                    the text description list items... also they cannot be empty
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

        # title object (doing this first for height calculation)
        self.font = pygame.font.Font(self.font_style, self.title_font_size)
        self.title_to_render = self.font.render(self.title, True, self.title_color)
        self.title_to_render_rect = self.title_to_render.get_rect()

        # calculating width and height for the pane box dimensions
        self.width = (self.tile_dims[0] * self.grid_dims[0]) + self.padding['l'] + self.padding['r'] + \
                     (self.tile_horizontal_spacing * (self.grid_dims[0] - 1))
        self.height = (self.tile_dims[1] * self.grid_dims[1]) + self.padding['t'] + self.padding['b'] + \
                      (self.tile_vertical_spacing * self.grid_dims[1]) + self.title_to_render.get_size()[1]

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
                
                very confusing 
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

        # debugging purposes
        print(f'''
            pos_x : {self.pos[0]}
            pos_y : {self.pos[1]}
            width : {self.width}
            height : {self.height}
            title_center : {self.title_to_render_rect.center}
            title_color : {self.title_color}
        
        ''')

    def __init_tile_tabs(self):
        # first i need to load the images for the buttons
        image_files = os.listdir(self.image_list_src)
        # TODO: order the image files by number index, seems like i could use a module for this

        # we will have an image list
        for img_file in image_files:
            cur_file = os.path.join(self.image_list_src, img_file)
            self.image_list.append(Graphic(cur_file, self.tile_dims, self.__screen))

        if not (len(self.image_list) == len(self.tag_list)):
            raise Exception(f'''
                The length of the image list does not correspond to the tag list (things will get buggy!)
                    image list: {self.image_list}
                    tag list: {self.tag_list}
            ''')

        for ind, img in enumerate(self.image_list):
            self.button_list.append(
                BasicButton(
                    self.tile_dims, self.pos, self.__screen, lambda x: self.tag_map[ind], toggle=True, border=5
                )
            )

    def render(self):
        pygame.draw.rect(self.__screen, self.gallery_background_color, self.pane_background_obj)
        self.__screen.blit(self.title_to_render, self.title_to_render_rect)

    def page_forward(self):
        pass

    def page_backward(self):
        pass
