import pygame

tile_size = 40
max_level = 3
screen_width = 1280
screen_height = 905


def load_level(filename):
    filename = "../levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    new_level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return new_level
