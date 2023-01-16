import sys

import pygame.key

from config import *
from functions import scroll_function, load_image, load_level
from location import draw_location
from groups import all_sprites, player_group

pygame.init()

screen = screen_initialize()

bg = pygame.image.load("data/Menu/level_choose/level_choose.png")
bg_rect = bg.get_rect()

width = bg.get_width()
height = bg.get_height()

button_x_size, button_y_size, font = buttons(140, 140, 65)


def display_buttons(button_image, button_rect):
    screen.blit(button_image, button_rect)


def level_choose():
    bg_rect[1] = -2100
    screen.blit(bg, bg_rect)

    button_images = [load_image("Menu/buttons/level_button.png"), load_image("Menu/buttons/level_button.png")]
    button_x_pos = 376
    button_y_pos = [570, 115]
    phase = 0

    # for i in range(9):
    #     button_y_pos = i * 180
    #     display_buttons(button_image, button_rect, button_x_pos, button_y_pos)
    #     button_collides.append(button_rect)
    #     button_texts.append(i + 1)

    pygame.display.update()

    while True:
        button_texts = []
        button_collides = []

        for i in range(2):
            button_rect = button_images[i].get_rect()
            button_rect.x, button_rect.y = button_x_pos, button_y_pos[i]
            display_buttons(button_images[i], button_rect)
            button_collides.append(button_rect)

        if phase == 0:
            button_texts = [1, 2]
        elif phase == 1:
            button_texts = [3, 4]
        elif phase == 2:
            button_texts = [5, 6]

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for elem in button_collides:
                collide = elem.collidepoint(mouse_pos)
                if collide:
                    level_number = button_texts[button_collides.index(elem)]
                    for el in all_sprites:
                        el.kill()
                    for el in player_group:
                        el.kill()
                    return draw_location(load_level(f'levels/level_{level_number}.txt'))

        if event.type == pygame.KEYDOWN:
            if phase == 2:
                scroll_amount = -920
            else:
                scroll_amount = -953
            if event.key == pygame.K_UP:
                if phase < 2:
                    if phase == 1:
                        scroll_amount = -920
                    phase += 1
                    scroll_function(screen, bg, bg_rect, abs(scroll_amount))
            elif event.key == pygame.K_DOWN:
                if phase > 0:
                    phase -= 1
                    scroll_function(screen, bg, bg_rect, scroll_amount)

            if event.key == pygame.K_i:
                sys.exit()

        pygame.display.update()

        clock.tick(MENU_FPS)
