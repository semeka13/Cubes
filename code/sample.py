#tile_images = {
#    'platform_1': load_image('platform_1.png'),
#    'killer_block': load_image('spikes.png')
#}
#player_image = load_image('player.png')

import pygame
import sys
from pygame.locals import *

pygame.init()
FPS = 60
size = WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def update():

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    elif key[pygame.K_SPACE] or key[pygame.K_RETURN]:
        print('игра начата')
        # начинаем игру
        return True


def start_screen():
    flag = True
    intro_text = ["Dungeon Master", "",
                  "Game rules: get to the finish line alive", "",
                  "Press <Enter> or <Space> to Start",
                  "Press <Esc> to Exit"]

    fon = pygame.transform.scale(pygame.image.load('../images/lava_bk.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 30)
    text_coord = HEIGHT // 4
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    run = True

    while run:
        update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(FPS)


start_screen()


"""
обозначение разных спрайтов
# - платфомы
. - пустота
@ - герой
+ - блок смерти
$ - финиш
"""
