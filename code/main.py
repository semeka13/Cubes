import sys

import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dungeon Master')

# define game variables
tile_size = 50

# load images
cave_img = pygame.image.load('../images/cave_bk.png')
lava_img = pygame.image.load('../images/lava_bk.png')


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class StartWindow:
    def update(self):
        intro_text = ["Dungeon Master", "",
                      "Game rules: get to the finish line alive", "",
                      "Press <Enter> to Start",
                      "Press <Esc> to Exit"]

        fon = pygame.transform.scale(pygame.image.load('../images/lava_bk.png'), (screen_width, screen_height))
        screen.blit(fon, (0, 0))
        font = pygame.font.SysFont(
            'sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 30)
        text_coord = screen_height // 4
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif key[pygame.K_RETURN]:
            print('игра начата')
            # начинаем игру
            return True


class Player:
    def __init__(self, x, y):
        player = pygame.image.load('../images/player.png')
        self.player = pygame.transform.scale(player, (40, 40))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.player.get_width()
        self.height = self.player.get_height()
        self.y_inc = 0
        self.jump = False
        self.in_air = True

    def update(self):
        x_change = 0
        y_change = 0

        key = pygame.key.get_pressed()
        if ((key[pygame.K_SPACE] and not self.jump) or
                (key[pygame.K_w] and not self.jump) or
                (key[pygame.K_UP] and not self.jump)) and not self.in_air:
            self.y_inc = -15
            self.jump = True
        if not key[pygame.K_SPACE] and not key[pygame.K_w] and not key[pygame.K_UP]:
            self.jump = False
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            x_change -= 5
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            x_change += 5

            # add gravity
        self.y_inc += 1
        if self.y_inc > 10:
            self.y_inc = 10
        y_change += self.y_inc
        # check for collision
        self.in_air = True
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + x_change, self.rect.y, self.width, self.height):
                x_change = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + y_change, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.y_inc < 0:
                    y_change = tile[1].bottom - self.rect.top
                    self.y_inc = 0
                # check if above the ground i.e. falling
                elif self.y_inc >= 0:
                    y_change = tile[1].top - self.rect.bottom
                    self.y_inc = 0
                    self.in_air = False

        # update player coordinates
        self.rect.x += x_change
        self.rect.y += y_change

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            y_change = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.left < 0:
            self.rect.left = 0

        # draw player onto screen
        screen.blit(self.player, self.rect)


class World:
    def world_plan(self, data):
        self.tile_list = []
        pos = 0
        # load images
        tile_images = {
           'platform_1': pygame.image.load('../images/platform_1.png'),
           'killer_block': pygame.image.load('../images/spikes.png')
        }

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '#':
                    img = pygame.transform.scale(tile_images['platform_1'], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == '@':
                    player_start_pos_x = col_count * tile_size
                    player_start_pos_y = row_count * tile_size
                    pos = (player_start_pos_x, player_start_pos_y)
                col_count += 1
            row_count += 1
        return pos

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


def load_level(filename):
    filename = "../levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    new_level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    print(new_level)
    return new_level


start_screen = StartWindow()
start_flag = True
world_data = load_level('level_test')
world = World()
player_pos = world.world_plan(world_data)
player = Player(*player_pos)
clock = pygame.time.Clock()

run = True
while run:
    screen.blit(lava_img, (0, 0))
    # screen.blit(sun_img, (100, 100))
    if start_flag:
        next = start_screen.update()
        if next:
            start_flag = False
    else:
        world.draw()
        player.update()
        # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)
pygame.quit()
