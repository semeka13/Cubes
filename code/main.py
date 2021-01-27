
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
score = 0
hp = 3
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
        screen.blit(data[img], (screen_width - (2 * tile_size) - (54 * img), screen_height - (18.5 * tile_size)))


def draw_hearts():
    heart_full = pygame.transform.scale(pygame.image.load('../images/heart.png'), (tile_size - 10, tile_size - 10))
    heart_empty = pygame.transform.scale(pygame.image.load('../images/heart_empty.png'), (tile_size - 10, tile_size - 10))
    data =  [heart_full] * hp + [heart_empty] * (3 - hp)
    for img in range(len(data)):
        screen.blit(data[img], (screen_width - (2 * tile_size) - (50 * img) + 5, screen_height - (19 * tile_size) - 10))


class StartWindow:
    def update(self):
        intro_text = "Dungeon Master"

        fon = pygame.transform.scale(pygame.image.load('../images/lava_bk.png'), (screen_width, screen_height))
        screen.blit(fon, (0, 0))
        font = pygame.font.SysFont(
            'sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 70)
        string_rendered = font.render(intro_text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = screen_width // 3 - 110
        intro_rect.y = screen_height // 7
        screen.blit(string_rendered, intro_rect)


class Button():
    def __init__(self, x, y, image_name, kx, ky):
        self.img = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.img, (tile_size * kx, tile_size * ky))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)
        return action


class Player:
    def __init__(self, x, y):
        self.player_image_l = pygame.transform.flip(pygame.image.load('../images/player.png'), True, False)
        self.player_image_r = pygame.image.load('../images/player.png')
        self.player = pygame.transform.scale(self.player_image_r, (40, 40))
        self.grave_img = pygame.transform.scale(pygame.image.load("../images/grave_2.png"), (75, 75))
        self.rect = self.player.get_rect()
        self.start_pos = (x, y)
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
        self.hp = 3
        self.jump_count = 0

    def update(self):
        x_change = 0
        y_change = 0

        if self.hp != 0:
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
            collisions = [enemy_group, death_tile_group]
            for group in collisions:
                if pygame.sprite.spritecollide(self, group, False):
                    pygame.time.wait(100)
                    self.hp -= 1
                    if self.hp != 0:
                        self.rect.x, self.rect.y = self.start_pos


            self.rect.x += x_change
            self.rect.y += y_change

            if self.rect.bottom > screen_height:
                self.rect.x, self.rect.y = self.start_pos
                self.hp -= 1

            if self.rect.right > screen_width:
                self.rect.right = screen_width

            if self.rect.top < 0:
                self.rect.top = 0

            if self.rect.left < 0:
                self.rect.left = 0
        elif self.hp == 0 and not self.dead:
            self.player = self.grave_img
            self.dead = True
            self.rect.y = (self.rect.y // tile_size) * tile_size - tile_size
        screen.blit(self.player, self.rect)
        return self.hp


class DeathTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('../images/lava_top.png'), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
                if tile == "-":
                    death_block_pos_x = col_count * tile_size
                    death_block_pos_y = row_count * tile_size
                    death_block = DeathTile(death_block_pos_x, death_block_pos_y)
                    death_tile_group.add(death_block)
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


death_tile_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
start_screen = StartWindow()
start_flag = True
world_data = load_level('level_test')
world = World()
player_pos = world.world_plan(world_data)
player = Player(*player_pos)
clock = pygame.time.Clock()
restart_button = Button(screen_width // 2 - 120, screen_height // 50, '../images/restart_button.png' , 2, 2)
exit_button = Button(screen_width // 2 + 20, screen_height // 50, '../images/exit_button.png', 2, 2)
start_button = Button(screen_width // 2 - 100, screen_height // 2 - 150, '../images/start_button.png', 4, 2)
exit_button_main = Button(screen_width // 2 - 100, screen_height // 2, '../images/exit_button_main.png', 4, 2)

run = True
while run:
    screen.blit(lava_img, (0, 0))
    if start_flag:
        next = start_screen.update()
        if start_button.draw():
            start_flag = False
        if exit_button_main.draw():
            run = False
    else:
        world.draw()

        if hp != 0:
            enemy_group.update()

        if hp == 0:
            if restart_button.draw():
                player = Player(*player_pos)
            if exit_button.draw():
                start_screen = StartWindow()
                start_flag = True
                player = Player(*player_pos)

        death_tile_group.draw(screen)
        coin_group.update()
        coin_group.draw(screen)
        score = collide_coin(score)
        enemy_group.draw(screen)
        draw_coins(score)
        draw_hearts()
        hp = player.update()
        # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)
pygame.quit()


