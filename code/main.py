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
game_over = False
score = 0
# load images
cave_img = pygame.image.load('../images/cave_bk.png')
lava_img = pygame.image.load('../images/lava_bk.png')


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def collide_coin(score):
    if pygame.sprite.spritecollide(player, coin_group, True):
        score += 1
    return score


def draw_coins(score):
    coin = pygame.transform.scale(pygame.image.load('../images/coin.png'), (tile_size, tile_size))
    coin_black = pygame.transform.scale(pygame.image.load('../images/coin_black.png'), (tile_size, tile_size))
    data = [coin_black] * (3 - score) + [coin] * score
    for img in range(len(data)):
        screen.blit(data[img], (screen_width - 100 - (50 * img), screen_height - 900))


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
            return True


class Player:
    def __init__(self, x, y):
        self.player_image_l = pygame.transform.flip(pygame.image.load('../images/player.png'), True, False)
        self.player_image_r = pygame.image.load('../images/player.png')
        self.player = pygame.transform.scale(self.player_image_r, (40, 40))
        self.grave_img = pygame.transform.scale(pygame.image.load("../images/grave_2.png"), (75, 75))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y - 20
        self.width = self.player.get_width()
        self.height = self.player.get_height()
        self.y_inc = 0
        self.jump = False
        self.in_air = True
        self.dead = False
        self.right_flip = False
        self.left_flip = False

    def update(self, game_over):
        x_change = 0
        y_change = 0

        if not game_over:
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
                self.left_flip = True
                self.right_flip = False
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                x_change += 5
                self.right_flip = True
                self.left_flip = False

            if self.left_flip:
                self.player = pygame.transform.scale(self.player_image_l, (40, 40))
            if self.right_flip:
                self.player = pygame.transform.scale(self.player_image_r, (40, 40))

            self.y_inc += 1
            if self.y_inc > 10:
                self.y_inc = 10
            y_change += self.y_inc
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x_change, self.rect.y, self.width, self.height):
                    x_change = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y_change, self.width, self.height):
                    if self.y_inc < 0:
                        y_change = tile[1].bottom - self.rect.top
                        self.y_inc = 0
                    elif self.y_inc >= 0:
                        y_change = tile[1].top - self.rect.bottom
                        self.y_inc = 0
                        self.in_air = False
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = True

            self.rect.x += x_change
            self.rect.y += y_change

            if self.rect.bottom > screen_height:
                self.rect.y = 0

            if self.rect.right > screen_width:
                self.rect.right = screen_width

            if self.rect.top < 0:
                self.rect.top = 0

            if self.rect.left < 0:
                self.rect.left = 0
        elif game_over and not self.dead:
            self.player = self.grave_img
            self.dead = True
            self.rect.y = (self.rect.y // tile_size) * tile_size - tile_size
        screen.blit(self.player, self.rect)
        return game_over


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_l = pygame.transform.flip(pygame.image.load('../images/enemy_3.png'), True, False)
        self.image_r = pygame.image.load('../images/enemy_3.png')
        self.image = pygame.transform.scale(self.image_r, (35, 55))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 5
        self.right_flip = True
        self.left_flip = False
        self.counter_r = 0
        self.counter_l = 0

    def update(self):
        if self.counter_r <= 100:
            self.rect.x += 1
            self.counter_r += 1
            self.right_flip = True
            self.left_flip = False
            if self.counter_r == 100:
                self.counter_l = 0
        elif self.counter_l <= 100:
            self.rect.x -= 1
            self.counter_l += 1
            self.right_flip = False
            self.left_flip = True
            if self.counter_l == 100:
                self.counter_r = 0

        if self.left_flip:
            self.image = pygame.transform.scale(self.image_l, (35, 55))
        if self.right_flip:
            self.image = pygame.transform.scale(self.image_r, (35, 55))


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('../images/coin.png')
        self.image = pygame.transform.scale(img, (tile_size - 10, tile_size - 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class EarnedCoins:
    def __init__(self, x, y):
        self.coin = pygame.image.load('../images/coin.png')


class Lifes():
    def __init__(self):
        image = pygame.image.load('../images/heart.png')
        image_empty = pygame.image.load('../images/heart_empty.png')
        self.heart_full = pygame.transform.scale(image, (tile_size - 10, tile_size - 10))
        self.heart_empty = pygame.transform.scale(image_empty, (tile_size - 10, tile_size - 10))

    def heart(self):
        screen.blit(self.heart_full, (screen_width - 100, screen_height - 960))
        screen.blit(self.heart_full, (screen_width - 150, screen_height - 960))
        screen.blit(self.heart_empty, (screen_width - 200, screen_height - 960))



class World:
    def world_plan(self, data):
        self.tile_list = []
        pos = 0
        tile_images = {
            'platform_1': pygame.image.load('../images/platform_1.png'),
            'killer_block': pygame.image.load('../images/spikes.png'),
            'platform_r_t': pygame.image.load('../images/platform_right_top_1.png'),
            'platform_l_t': pygame.image.load('../images/platform_left_top.png')
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
                if tile == '(':
                    img = pygame.transform.scale(tile_images['platform_l_t'], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == ')':
                    img = pygame.transform.scale(tile_images['platform_r_t'], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == '@':
                    player_start_pos_x = col_count * tile_size
                    player_start_pos_y = row_count * tile_size
                    pos = (player_start_pos_x, player_start_pos_y)
                if tile == "!":
                    enemy_start_pos_x = col_count * tile_size
                    enemy_start_pos_y = row_count * tile_size - 10
                    enemy = Enemy(enemy_start_pos_x, enemy_start_pos_y)
                    enemy_group.add(enemy)
                if tile == "$":
                    coin_pos_x = col_count * tile_size
                    coin_pos_y = row_count * tile_size + 20
                    coin = Coin(coin_pos_x, coin_pos_y)
                    coin_group.add(coin)
                col_count += 1
            row_count += 1
        return pos

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


def load_level(filename):
    filename = "../levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    new_level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    print(new_level)
    return new_level


coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
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
    if start_flag:
        next = start_screen.update()
        if next:
            start_flag = False
    else:
        world.draw()

        if not game_over:
            enemy_group.update()
        coin_group.update()
        coin_group.draw(screen)
        score = collide_coin(score)
        enemy_group.draw(screen)
        game_over = player.update(game_over)
        # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)
pygame.quit()
