import pygame, sys, os
# sys.path.append(os.getcwd())
from internal.PygameApp import Screen, Graphic, AnimationSequence
from widgets.BasicMenuBar import BasicMenuBar
from widgets.BasicButton import BasicButton
from widgets.BasicGalleryOptions import BasicGalleryOptions

clock = pygame.time.Clock()

'''
    Map Maker screen structure:
        - sidebar with menu options
        - toggle select different block types
            - from selection, we can manipulate what is actually being made on the map
        - close/ open the sidebar (challenging)

    this thing will immediately anchor itself to the top corner of screen
'''


class MapMakerPane:
    def __init__(self, dims, screen, map_sprite_folder=None, background_color=(255, 255, 255), show=True):
        self.width = dims[0] if dims[0] >= 1 else screen.width * dims[0]
        self.height = dims[1] if dims[1] >= 1 else screen.height * dims[1]
        self.sprite_folder = map_sprite_folder
        self.background_color = background_color
        self.show = show

        # TODO: make a list of image representable sprites (so much work)

        # make some default graphics here
        if self.sprite_folder:
            pass


def action():
    print('action time!')


@Screen
def map_maker_screen(size, screen):
    menu = BasicMenuBar(
        screen, 100, 100, menu_items=['reset', 'load', 'save', 'back'], menu_actions=[action, action, action, action],
        font_color=(255, 255, 255, 0), font_size=15, menu_background_color=(0, 0, 0, 1)
    )

    # btn = BasicButton(
    #     (100, 100), (100, 100), screen, action, src='man_idle.png',
    #     border=5, border_color=(0, 255, 0), active_color=(255, 255, 255), active_border_color=(255, 0, 0),
    #     cursor=True, toggle=False
    # )

    sample_graphic = Graphic('../tests/man_idle.png', (100, 100), screen)

    anim_seq = [Graphic('../tests/man_idle.png', (100, 100), screen),
                Graphic('../tests/man_idle.png', (100, 100), screen),
                Graphic('../tests/man_idle.png', (100, 100), screen)]

    anim = AnimationSequence(
        (100, 100), screen, src_folder='../tests/test_animation_files'
    )

    print(anim.head)

    gallery = BasicGalleryOptions(
        (75, 75), (0, 0), screen, image_list_src='../internal/game_files/map_tiles/default_sprites/tileset_default',
        tag_list=[0,0,0,0,0,0,0,0,0],text_description_list=['white block','red block','green block','r','r','r','r','r','r'],
        title='Select', font_size=10, tile_vertical_spacing=20, page_arrow_size=20, page_arrow_border_color=(0, 0, 0),
        page_arrow_border=2
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
                    menu.set_active_toggle(1)
                elif event.key == pygame.K_UP:
                    menu.set_active_toggle(-1)
                elif event.key == pygame.K_SPACE:
                    menu.execute_action_toggle()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('click')

        gallery.render()
        # menu.render()

        if not running:
            break

        pygame.display.flip()

    pygame.quit()
