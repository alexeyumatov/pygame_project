import sys

import pygame.key

from config import *
from functions import scroll_function, load_image, load_level
from location import draw_location
from groups import all_sprites, player_group, enemies_group
from db_functions import levels_amount_select

pygame.init()

screen = screen_initialize()

bg = pygame.image.load("data/Menu/level_choose/level_choose.png")
bg_rect = bg.get_rect()

width = bg.get_width()
height = bg.get_height()

market_rect = pygame.Rect((879, 495, 620, 490))
market = pygame.Surface((620, 490))
market.fill(white)
market.set_alpha(0)

button_x_size, button_y_size, font = buttons(140, 140, 65)


def display_buttons(button_image, button_rect):
    screen.blit(button_image, button_rect)


def level_choose():
    bg_rect[1] = -2100
    screen.blit(bg, bg_rect)

    button_images = [load_image(f"Menu/buttons/numbered_buttons/level_button_{i}.png") for i in range(1, 14)]
    button_images.append(load_image("Menu/buttons/locked_level_button.png"))
    button_x_pos = 376
    button_y_pos = [570, 115]
    phase = 0
    levels_amount = levels_amount_select(1)
    button_texts = [i for i in range(1, levels_amount + 1)]
    if len(button_texts) < 6:
        locked_levels = 6 - levels_amount
        for i in range(locked_levels):
            button_texts.append(0)

    while True:
        button_collides = []
        btn = []

        if phase == 0:
            btn = button_texts[0:2]
            screen.blit(market, market_rect)
        elif phase == 1:
            btn = button_texts[2:4]
        elif phase == 2:
            btn = button_texts[4:6]

        for i in range(2):
            if btn[i] > 0:
                button_image = button_images[btn[i] - 1]
            else:
                button_image = button_images[-1]
            button_rect = button_image.get_rect()
            button_rect.x, button_rect.y = button_x_pos, button_y_pos[i]
            display_buttons(button_image, button_rect)
            if btn[i] > 0:
                button_collides.append(button_rect)

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for elem in button_collides:
                collide = elem.collidepoint(mouse_pos)
                if collide:
                    level_number = btn[button_collides.index(elem)]
                    for el in all_sprites:
                        el.kill()
                    for el in player_group:
                        el.kill()
                    for el in enemies_group:
                        el.kill()
                    draw_location(load_level(f'levels/level_{level_number}.txt'))
                    return level_number
            market_coolide = market_rect.collidepoint(mouse_pos)
            if market_coolide:
                return market_window()

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


def market_window():
    screen.fill((0, 30, 38))

    while True:
        event = pygame.event.poll()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return level_choose()

        pygame.display.update()


