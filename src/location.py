from functions import load_image
from groups import *
from objects import Coin
from enemies_config import RegularEnemy


tile_images = {
    'left_wall': load_image('Locations/Left_Wall.png'),
    'right_wall': load_image('Locations/Right_Wall.png'),
    'roof': load_image('Locations/Roof.png'),
    'ladder': load_image('Locations/Ladder.png'),
    'floor': load_image('Locations/Floor.png'),
    'bottom_left_corner': load_image('Locations/Bottom_Left_Corner.png'),
    'bottom_right_corner': load_image('Locations/Bottom_Right_Corner.png'),
    'top_left_corner': load_image('Locations/Top_Left_Corner.png'),
    'top_right_corner': load_image('Locations/Top_Right_Corner.png'),
    'dark_block': load_image('Locations/Dark_Block.png'),
    'platform': load_image('Locations/Platform.png'),
    'left_platform_corner': load_image('Locations/Left_Platform_Corner.png'),
    'right_platform_corner': load_image('Locations/Right_Platform_Corner.png'),
    'top_left_exit': load_image('Locations/1_PART.png'),
    'top_right_exit': load_image('Locations/2_PART.png'),
    'main_left_exit': load_image('Locations/3_PART.png'),
    'main_right_exit': load_image('Locations/4_PART.png')
}

tile_width = tile_height = 128


def draw_location(level_map):
    x, y = None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                pass
            elif level_map[y][x] == '+':
                Tile('dark_block', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '{':
                Tile('top_left_corner', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '-':
                Tile('roof', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '}':
                Tile('top_right_corner', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '$':
                Tile('left_wall', x, y, all_sprites, tiles_group, walls_group)
            elif level_map[y][x] == '[':
                Tile('bottom_left_corner', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '_':
                Tile('floor', x, y, all_sprites, tiles_group, floor_group)
            elif level_map[y][x] == ']':
                Tile('bottom_right_corner', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '/':
                Tile('right_wall', x, y, all_sprites, tiles_group, walls_group)
            elif level_map[y][x] == '|':
                Tile('ladder', x, y, all_sprites, ladder_group)
            elif level_map[y][x] == ':':
                Tile('left_platform_corner', x, y, all_sprites, tiles_group, walls_group)
            elif level_map[y][x] == ';':
                Tile('right_platform_corner', x, y, all_sprites, tiles_group, walls_group)
            elif level_map[y][x] == '\"':
                Tile('platform', x, y, all_sprites, tiles_group, floor_group, walls_group)
            elif level_map[y][x] == '#':
                Tile('top_left_exit', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '№':
                Tile('top_right_exit', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '!':
                Tile('main_left_exit', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '&':
                Tile('main_right_exit', x, y, all_sprites, tiles_group)
            elif level_map[y][x] == '^':
                Coin(x, y, all_sprites, coins_group)
            elif level_map[y][x] == 'E':
                RegularEnemy(x, y, all_sprites, enemies_group)
    return x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super(Tile, self).__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
