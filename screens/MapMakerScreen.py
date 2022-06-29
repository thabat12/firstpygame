import pygame, sys, os
# sys.path.append(os.getcwd())
from internal.PygameApp import Screen, Graphic, AnimationSequence
# from widgets.BasicGalleryOptions import BasicGalleryOptions
from widgets.basic_widgets import BasicButton, BasicMenuBar, BasicGalleryOptions

clock = pygame.time.Clock()

'''
    Map Maker screen structure:
        - sidebar with menu options
        - toggle select different block types
            - from selection, we can manipulate what is actually being made on the map
        - close/ open the sidebar (challenging)

    this thing will immediately anchor itself to the top corner of screen
'''


# im lazy implementing here because this screen does not have to be hyper general like the widgets i made, so there will
# be less parameters and more hard coding in the screens
class MapMakerPane:
    def __init__(self, dims, pos, screen, map_sprite_folder=None, background_color=(255, 255, 255), show=True,
                 title=''):
        # TODO: make validation method for valid sprite folders in PygameApp.py (good for debugging)
        if not os.path.isdir(map_sprite_folder):
            raise Exception(f'''
                Invalid directory for map sprite folder:
                    {map_sprite_folder}
            ''')

        # handle dims
        self.width = dims[0] if dims[0] > 1 else int(screen.get_size()[0] * dims[0])
        self.height = dims[1] if dims[1] > 1 else int(screen.get_size()[1] * dims[1])
        self.pos = pos
        self.__screen = screen
        self.sprite_folder = map_sprite_folder
        self.background_color = background_color
        # hide or show the screen, maybe even have a sidebar that can scroll around (challenging)
        self.show = show

        self.rect_object = pygame.rect.Rect(self.pos, (self.width, self.height))

        menu_items = [
            'reset',
            'save',
            'load',
            'back'
        ]

        # poorly implemented ):
        menu_actions = [
            lambda: 'reset',
            lambda: 'save',
            lambda: 'load',
            lambda: print('back')
        ]

        menu_width = int(self.width * 0.6)
        menu_height = 200
        menu_top_offset = 20

    def render(self):
        pygame.draw.rect(self.__screen, self.background_color, self.rect_object)
        self.menu.render()


def action():
    print('action time!')


@Screen
def map_maker_screen(size, screen):
    # menu = BasicMenuBar(
    #     screen, 100, 100, menu_items=['reset', 'load', 'save', 'back'], menu_actions=[action, action, action, action],
    #     font_color=(255, 255, 255, 0), font_size=15, menu_background_color=(0, 0, 0, 1)
    # )

    # btn = BasicButton(
    #     (100, 100), (100, 100), screen, action, src='man_idle.png',
    #     border=5, border_color=(0, 255, 0), active_color=(255, 255, 255), active_border_color=(255, 0, 0),
    #     cursor=True, toggle=False
    # )

    button = BasicButton(
        (100, 100), (100, 100), screen, background_color=(255, 255, 255, 100), title='button',
        src='../internal/game_files/map_tiles/default_sprites/tileset_default/red_solid2.png',
        padding={'t': 10, 'b': 10, 'l': 10, 'r': 10}, title_color=(255, 255, 255), border=4, toggle=False,
        action=lambda: print('action executed')
    )

    menu = BasicMenuBar(
        (150, 150), (100, 100), screen, title='Menu', menu_text_list=['save', 'load', 'hi'],
        menu_actions=[lambda: None, lambda: print('googoogaga'), lambda: None], font_color=(0, 0, 0),
        active_font_color=(255, 0, 0),
        background_color=(255, 255, 255), menu_item_spacing=4, padding={'t': 10, 'b': 10, 'l': 10, 'r': 10},
        title_size=20, title_item_spacing=10
    )

    sample_graphic = Graphic('../tests/man_idle.png', (100, 100), screen)

    anim_seq = [Graphic('../tests/man_idle.png', (100, 100), screen),
                Graphic('../tests/man_idle.png', (100, 100), screen),
                Graphic('../tests/man_idle.png', (100, 100), screen)]

    anim = AnimationSequence(
        (100, 100), screen, src_folder='../tests/test_animation_files'
    )

    gallery = BasicGalleryOptions(
        (75, 75), (0, 0), screen, image_list_src='../internal/game_files/map_tiles/default_sprites/tileset_default',
        tag_list=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        text_description_list=['white block', 'red block', 'green block', 'r', 'r', 'r', 'r', 'r', 'r'],
        title='Select', font_size=10, tile_vertical_spacing=20, page_arrow_size=20, page_arrow_border_color=(0, 0, 0),
        page_arrow_border=2, is_toggle=True, grid_dims=(3, 3), tile_border=4, tile_border_color=(255, 255, 255),
        tile_active_border_color=(255, 0, 0)
    )

    running = True

    while 1:
        clock.tick(60)

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    continue
                elif event.key == pygame.K_UP:
                    continue
                elif event.key == pygame.K_SPACE:
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button.click()
                    print(gallery.click())
                    menu.click()

        gallery.render()
        menu.render()
        # pane.render()
        button.render()

        if not running:
            break

        pygame.display.flip()

    pygame.quit()
