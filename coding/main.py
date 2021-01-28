import sys

from coding.sprites import *
import pygame
from pygame.locals import *

from coding import *

score = 0
hp = 3
cur_level = 1
next_level = False

pygame.init()

pygame.display.set_caption('Dungeon Master')


def reset_world(level):
    door_group.empty()
    enemy_group.empty()
    coin_group.empty()
    death_tile_group.empty()
    level_data = load_level(f"level_{level}")
    return level_data


def collide_coin(score):
    if pygame.sprite.spritecollide(player, coin_group, True):
        score += 1
    return score


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def draw_coins(score):
    coin = pygame.transform.scale(pygame.image.load('../images/coin.png'), (tile_size, tile_size))
    coin_black = pygame.transform.scale(pygame.image.load('../images/coin_black.png'), (tile_size, tile_size))
    data = [coin_black] * (3 - score) + [coin] * score
    for img in range(len(data)):
        screen.blit(data[img], (screen_width - (2 * tile_size) - (54 * img), screen_height - (20.5 * tile_size)))


def draw_hearts():
    heart_full = pygame.transform.scale(pygame.image.load('../images/heart.png'), (tile_size - 5, tile_size - 5))
    heart_empty = pygame.transform.scale(pygame.image.load('../images/heart_empty.png'), (tile_size - 5, tile_size - 5))
    data = [heart_full] * hp + [heart_empty] * (3 - hp)
    for img in range(len(data)):
        screen.blit(data[img], (screen_width - (2 * tile_size) - (50 * img) + 5, screen_height - (21.5 * tile_size)))


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


class LevelMenu:
    def update(self):
        intro_text = "Dungeon Master"

        fon = pygame.transform.scale(pygame.image.load('../images/lava_bk.png'), (screen_width, screen_height))
        screen.blit(fon, (0, 0))
        """font = pygame.font.SysFont(
            'sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 70)
        string_rendered = font.render(intro_text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = screen_width // 3 - 110
        intro_rect.y = screen_height // 7
        screen.blit(string_rendered, intro_rect)"""


class Button:
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
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)
        return action


class Player:
    def __init__(self, x, y, hp=3):
        self.player_image_l = pygame.transform.flip(pygame.image.load('../images/player.png'), True, False)
        self.player_image_r = pygame.image.load('../images/player.png')
        self.player_height = 40
        self.player = pygame.transform.scale(self.player_image_r, (tile_size - 3, tile_size - 3))
        self.grave_img = pygame.transform.scale(pygame.image.load("../images/grave_2.png"),
                                                (tile_size + 10, tile_size + 10))
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
        self.hp = hp
        self.jump_count = 0
        self.next_level = False

    def update(self):
        x_change = 0
        y_change = 0
        col_thresh = 20

        if self.hp != 0:
            key = pygame.key.get_pressed()
            if ((key[pygame.K_SPACE] and not self.jump) or
                (key[pygame.K_w] and not self.jump) or
                (key[pygame.K_UP] and not self.jump)) and not self.in_air:
                self.y_inc = -14
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
                self.player = pygame.transform.scale(self.player_image_l, (tile_size - 3, tile_size - 3))
            if self.right_flip:
                self.player = pygame.transform.scale(self.player_image_r, (tile_size - 3, tile_size - 3))

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
            if pygame.sprite.spritecollide(self, door_group, False):
                pygame.time.wait(100)
                self.next_level = True

            for platform in moving_platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.rect.x + x_change, self.rect.y, self.width, self.height):
                    x_change = 0
                # collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + y_change, self.width, self.height):
                    # check if below platform
                    if abs((self.rect.top + y_change) - platform.rect.bottom) < col_thresh:
                        self.y_inc = 0
                        y_change = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + y_change) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        y_change = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.dir_move
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
        return self.hp, self.next_level


class World:
    def add_tile(self, name, col_count, row_count):
        tile_images = {
            'platform_1': pygame.image.load('../images/platform_1.png'),
            'killer_block': pygame.image.load('../images/spikes.png'),
            'platform_r_t': pygame.image.load('../images/platform_right_top_1.png'),
            'platform_l_t': pygame.image.load('../images/platform_left_top.png'),
            'platform_c': pygame.image.load('../images/platform_center.png'),
            'platform_long': pygame.image.load('../images/platform_long.png')
        }
        img = pygame.transform.scale(tile_images[name], (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x = col_count * tile_size
        img_rect.y = row_count * tile_size
        tile = (img, img_rect)
        self.tile_list.append(tile)

    def world_plan(self, data):
        self.tile_list = []
        pos = 0
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '#':
                    self.add_tile('platform_1', col_count, row_count)
                if tile == '|':
                    self.add_tile('platform_long', col_count, row_count)
                if tile == '_':
                    self.add_tile('platform_c', col_count, row_count)
                if tile == '(':
                    self.add_tile('platform_l_t', col_count, row_count)
                if tile == ')':
                    self.add_tile('platform_r_t', col_count, row_count)
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
                if tile == "0":
                    door_pos_x = col_count * tile_size
                    door_pos_y = row_count * tile_size
                    door = Door(door_pos_x, door_pos_y)
                    door_group.add(door)
                if tile == "&":
                    moving_platform_pos_x = col_count * tile_size
                    moving_platform_pos_y = row_count * tile_size
                    moving_platform = MovingPlatform(moving_platform_pos_x, moving_platform_pos_y, 1, 0)
                    moving_platform_group.add(moving_platform)
                col_count += 1
            row_count += 1
        return pos

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


screen = pygame.display.set_mode((screen_width, screen_height))
door_group = pygame.sprite.Group()
death_tile_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
moving_platform_group = pygame.sprite.Group()

start_screen = StartWindow()
menu_screen = LevelMenu()

world_data = load_level('level_test')
world = World()
player_pos = world.world_plan(world_data)
player = Player(*player_pos)
clock = pygame.time.Clock()

restart_button = Button(screen_width // 2 - 120, screen_height // 50, '../images/restart_button.png', 2, 2)
exit_button = Button(screen_width // 2 + 20, screen_height // 50, '../images/exit_button.png', 2, 2)
start_button = Button(screen_width // 2 - 125, screen_height // 2 - 100, '../images/start_button.png', 7, 3)
exit_button_main = Button(screen_width // 2 - 125, screen_height // 2 + 50, '../images/exit_button_main.png', 7, 3)
exit_button_level = Button(screen_width // 30, screen_height // 30, '../images/exit_button_main.png', 7, 3)
level_1 = Button(screen_width // 10, screen_height // 4, '../images/start_button.png', 7, 3)
level_2 = Button(screen_width // 2.5, screen_height // 4, '../images/start_button.png', 7, 3)
level_3 = Button(screen_width // 1.5 + 30, screen_height // 4, '../images/start_button.png', 7, 3)
level_4 = Button(screen_width // 10, screen_height // 2, '../images/start_button.png', 7, 3)
level_5 = Button(screen_width // 2.5, screen_height // 2, '../images/start_button.png', 7, 3)
level_6 = Button(screen_width // 1.5 + 30, screen_height // 2, '../images/start_button.png', 7, 3)

run = True
lava_img = pygame.transform.scale(pygame.image.load('../images/lava_bk.png'), (screen_width, screen_height))
start_flag = 0
game_start = False
while run:
    screen.blit(lava_img, (0, 0))
    if start_flag == 0:
        start_screen.update()
        if start_button.draw():
            start_flag += 1
        if exit_button_main.draw():
            run = False
    if start_flag == 1:
        menu_screen.update()
        if level_1.draw():
            world_data = reset_world(1)
            start_flag += 1
            game_start = True
        if level_2.draw():
            world_data = reset_world(2)
            start_flag += 1
            game_start = True
        if level_3.draw():
            world_data = reset_world(3)
            start_flag += 1
            game_start = True
        if level_4.draw():
            world_data = reset_world(4)
            start_flag += 1
            game_start = True
        if level_5.draw():
            world_data = reset_world(5)
            start_flag += 1
            game_start = True
        if level_6.draw():
            world_data = reset_world(6)
            start_flag += 1
            game_start = True

        if exit_button_level.draw():
            start_flag = 0

    elif start_flag == 2:
        if game_start:
            world = World()
            player_pos = world.world_plan(world_data)
            player = Player(*player_pos, hp=hp)
            game_start = False
        world.draw()
        death_tile_group.draw(screen)
        moving_platform_group.draw(screen)

        door_group.draw(screen)

        coin_group.update()
        coin_group.draw(screen)

        score = collide_coin(score)
        enemy_group.draw(screen)
        draw_coins(score)
        draw_hearts()
        hp, next_level = player.update()
        # draw_grid()
        if hp != 0:
            moving_platform_group.update()
            enemy_group.update()

        if hp == 0:
            if restart_button.draw():
                hp = 3
                player = Player(*player_pos, hp=hp)
            if exit_button.draw():
                player = Player(*player_pos, hp=3)
                start_screen = StartWindow()
                start_flag -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)
pygame.quit()
