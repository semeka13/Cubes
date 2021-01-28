import pygame

from coding import *


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('../images/finish_1.png')
        self.image = pygame.transform.scale(img, (int(tile_size * 1.1), int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x - 3
        self.rect.y = y - 20


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('../images/coin.png')
        self.image = pygame.transform.scale(img, (tile_size - 4, tile_size - 4))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class DeathTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('../images/lava_top.png'), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, name,  x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(name)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count_move = 0
        self.dir_move = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.dir_move * self.move_x
        self.rect.y += self.dir_move * self.move_y
        self.count_move += 1
        if abs(self.count_move) > 50:
            self.dir_move *= -1
            self.count_move *= -1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_l = pygame.transform.flip(pygame.image.load('../images/enemy_3.png'), True, False)
        self.image_r = pygame.image.load('../images/enemy_3.png')
        self.size_x = tile_size - 7
        self.size_y = tile_size + 7
        self.image = pygame.transform.scale(self.image_r, (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 2
        self.right_flip = True
        self.left_flip = False
        self.counter_r = 0
        self.counter_l = 0

    def update(self):
        if self.counter_r <= tile_size * 2:
            self.rect.x += 1
            self.counter_r += 1
            self.right_flip = True
            self.left_flip = False
            if self.counter_r == tile_size * 2:
                self.counter_l = -1
        elif self.counter_l <= tile_size * 2:
            self.rect.x -= 1
            self.counter_l += 1
            self.right_flip = False
            self.left_flip = True
            if self.counter_l == tile_size * 2:
                self.counter_r = 0

        if self.left_flip:
            self.image = pygame.transform.scale(self.image_l, (self.size_x, self.size_y))
        if self.right_flip:
            self.image = pygame.transform.scale(self.image_r, (self.size_x, self.size_y))
