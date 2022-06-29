import internal.PygameApp as game_app
import os

path = '../internal/game_files/map_tiles/default_sprites/tileset_default'
img_paths = os.listdir(path)

print(game_app.order_files_by_index(img_paths))