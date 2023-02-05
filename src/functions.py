import os
import sys

from config import *
from groups import all_sprites, player_group, enemies_group

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(name):
    fullname = 'data/' + name
    with open(fullname, 'r', encoding='utf-8') as level:
        level_map = [line.rstrip('\n') for line in level]
    return level_map


def flip(image):
    image = pygame.transform.flip(image, True, False)
    return image


def display_buttons(button_rect, button_text, button_x_pos, button_y_pos, text):
    pygame.draw.rect(screen, (255, 255, 255), button_rect)
    if len(text) <= 5:
        screen.blit(button_text, (button_x_pos - 40, button_y_pos - 25))
    elif len(text) <= 8:
        screen.blit(button_text, (button_x_pos - 75, button_y_pos - 25))
    else:
        screen.blit(button_text, (button_x_pos - 130, button_y_pos - 25))


def scroll_function(screenSurf, bg, bg_rect, offsetY):
    bg_rect[1] += offsetY
    if abs(bg_rect[1]) >= 6450:
        bg_rect[1] = -6450
    if bg_rect[1] > 0:
        bg_rect[1] = 0
    screenSurf.blit(bg, bg_rect)


def draw_pause():
    button_x_size, button_y_size, font = buttons(350, 70, 35)
    button_collides = []
    button_texts = []
    width, height = resolution
    surf = pygame.Surface(resolution)
    surf.fill(black)
    surf.set_alpha(120)
    screen.blit(surf, (0, 0))

    for i in range(3):
        button_x_pos = width / 2
        button_y_pos = width / (5 - i) + 50
        button_rect = pygame.Rect(button_x_pos,
                                  button_y_pos, 0, 0).inflate(button_x_size,
                                                              button_y_size)
        button_text = ''
        text = ''

        if i == 0:
            button_text = font.render('Resume', True, black)
            text = 'resume'
        elif i == 1:
            button_text = font.render('Options', True, black)
            text = 'options'
        elif i == 2:
            button_text = font.render('Exit', True, black)
            text = 'exit'

        button_texts.append(text)
        button_collides.append(button_rect)

        display_buttons(button_rect, button_text, button_x_pos, button_y_pos,
                        text)
    pygame.display.update()
    return button_collides, button_texts


def display_player_data(hero, ultimate_attack, hero_is_poisoned=False):
    hp_data = data_font.render(str(hero.health_points), True, white)
    shield_data = data_font.render(str(hero.shield_points), True, white)
    if hero.stamina == 100 and ultimate_attack:
        screen.blit(ultimate_ready, (900, 955))
        stamina_data = data_font.render('In Use', True, white)
    elif hero.stamina == 100:
        stamina_data = data_font.render('Ready', True, white)
        screen.blit(ultimate_ready, (900, 955))
    else:
        stamina_data = data_font.render(str(hero.stamina), True, white)
        screen.blit(ultimate_not_ready, (900, 955))
    screen.blit(hp_data, (690, 987))
    if hero_is_poisoned:
        screen.blit(poisoned_heart, (600, 970))
    else:
        screen.blit(heart, (600, 970))
    screen.blit(shield_data, (1290, 987))
    screen.blit(shield, (1200, 970))
    screen.blit(stamina_data, (1006, 987))


def draw_death_screen_buttons():
    # BUTTONS
    buttons_rect = [pygame.Rect(627, 600, 656, 132), pygame.Rect(627, 840, 656, 132)]
    buttons = [pygame.Surface((656, 132)), pygame.Surface((656, 132))]
    for el in buttons:
        el.set_alpha(0)
    for i in range(len(buttons)):
        screen.blit(buttons[i], buttons_rect[i])

    return buttons_rect


def draw_window():
    screen.fill(level_color)
    for el in all_sprites:
        screen.blit(el.image, camera.apply(el))
    for el in player_group:
        screen.blit(el.image, camera.apply(el))
    for el in enemies_group:
        screen.blit(el.image, camera.apply(el))

