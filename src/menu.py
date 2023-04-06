import sys

import pygame.image

from src.config import *
from src.functions import display_buttons, draw_pause, draw_window, load_image, \
    draw_death_screen_buttons, draw_options_texts, main_melody, game_melody
from src.level_choose_screen import level_choose
from src.tips import settings_tip, restart_game_tip
from src.groups import all_sprites, player_group, enemies_group
from src.db_functions import tips_update, hands_detection_update, music_update, \
    tips_select, hands_detection_select, music_select

pygame.init()

screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN | pygame.SCALED,
                                 vsync=1)
width = screen.get_width()
height = screen.get_height()

pygame.mixer.music.set_volume(0.12)
main_melody()

screen.fill(level_color)

button_x_size, button_y_size, font = buttons(350, 70, 35)


# START SCREEN FUNCTION
def start_screen():
    screen.fill(level_color)
    button_collides = []
    button_texts = []
    animCount = 0
    background = [load_image(f'Menu/main_menu/{i}.png') for i in range(1, 9)]

    while True:
        if animCount + 1 >= 56:
            animCount = 0

        screen.blit(background[animCount // 7], (0, 0))
        animCount += 1

        # BUTTON GENERATION
        for i in range(3):
            button_x_pos = width / 2
            button_y_pos = width / (5 - i) + 50
            button_rect = pygame.Rect(button_x_pos,
                                      button_y_pos, 0, 0
                                      ).inflate(button_x_size, button_y_size)
            button_text = ''
            text = ''

            if i == 0:
                button_text = font.render('Play', True, black)
                text = 'play'
            elif i == 1:
                button_text = font.render('Options', True, black)
                text = 'options'
            elif i == 2:
                button_text = font.render('Exit', True, black)
                text = 'exit'

            button_texts.append(text)
            button_collides.append(button_rect)

            display_buttons(button_rect, button_text, button_x_pos,
                            button_y_pos, text)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "play":
                            screen.fill((0, 30, 38))
                            return level_choose()
                        elif text == "options":
                            screen.fill((0, 30, 38))
                            return options_screen(False)
                        elif text == "exit":
                            quit()

        pygame.display.update()
        clock.tick(FPS)


# PAUSE FUNCTION
def pause():
    paused = True
    draw_window()
    button_collides, button_texts = draw_pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "resume":
                            return text
                        elif text == "options":
                            main_melody()
                            return options_screen(True)
                        elif text == "exit":
                            main_melody()
                            return start_screen()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        clock.tick(MENU_FPS)


button_collides = []
button_texts = []


def death_screen():
    dead = True
    screenAnim = 0
    background = [load_image(f'Menu/death_screen/'
                             f'Death_Screen{i}.png', -1) for i in range(1, 9)]
    background_color = pygame.Surface(resolution)
    background_color.fill(red)
    background_color.set_alpha(80)
    draw_window()
    screen.blit(background_color, (0, 0))
    pygame.display.update()

    while dead:
        if screenAnim >= 56:
            screenAnim = 0

        background_image = background[screenAnim // 7]
        screenAnim += 1
        screen.blit(background_image, (0, 0))
        buttons_rect = draw_death_screen_buttons()

        pygame.display.update()

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for elem in buttons_rect:
                collided = elem.collidepoint(mouse_pos)

                if collided:
                    for el in all_sprites:
                        el.kill()
                    for el in player_group:
                        el.kill()
                    for el in enemies_group:
                        el.kill()
                    main_melody()
                    if buttons_rect.index(elem) == 0:
                        return level_choose()
                    else:
                        return start_screen()
        clock.tick(FPS)


def options_screen(from_pause):
    screen.fill((0, 30, 38))
    button_on = pygame.image.load('src/data/settings/Settings_button_on.png')
    button_off = pygame.image.load('src/data/settings/Settings_button_off.png')
    buttons_information = ['on' if tips_select() else 'off',
                           'on' if music_select() else 'off',
                           'on' if hands_detection_select() else 'off']
    buttons_on_screen = []
    for i in range(1, len(buttons_information) + 1):
        if buttons_information[i - 1] == 'on':
            screen.blit(button_on, (700, 250 * i))
        else:
            screen.blit(button_off, (700, 250 * i))
        buttons_on_screen.append(pygame.Rect(700, 250 * i, 300, 90))

    header = header_font.render('OPTIONS', True, white)
    screen.blit(header, (820, 48))
    settings_tip()
    draw_options_texts()
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if from_pause:
                        game_melody()
                        return pause()
                    else:
                        return start_screen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for key, button in enumerate(buttons_on_screen):
                    if button.collidepoint(mouse_pos):
                        state = True
                        if buttons_information[key] == 'on':
                            buttons_information[key] = 'off'
                        else:
                            buttons_information[key] = 'on'
                            state = False
                        if key == 0:
                            tips_update(state)
                        elif key == 1:
                            music_update(state)
                            main_melody()
                        elif key == 2:
                            hands_detection_update(state)
                            restart_game_tip()
                        buttons_on_screen.clear()
                        for i in range(1, len(buttons_information) + 1):
                            if buttons_information[i - 1] == 'on':
                                screen.blit(button_on, (700, 250 * i))
                            else:
                                screen.blit(button_off, (700, 250 * i))
                            buttons_on_screen.append(pygame.Rect(700,
                                                                 250 * i,
                                                                 300, 90))

        pygame.display.update()
        clock.tick(MENU_FPS)
