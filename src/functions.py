import pygame
import os
import sys

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


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

