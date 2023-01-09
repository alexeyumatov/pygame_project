import os
import sys

import pygame

from config import *
from groups import all_sprites

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


def scroll_function(screenSurf, bg, bg_rect, offsetY):
    bg_rect[1] += offsetY
    if abs(bg_rect[1]) >= 2100:
        bg_rect[1] = -2100
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


def draw_window():
    screen.fill(level_color)
    for el in all_sprites:
        screen.blit(el.image, camera.apply(el))
    pygame.display.flip()


# def hands_detection():
#     cords = {}
#     last_status, hand_type = "", ""
#     success, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#
#     imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#     imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
#
#     if results.multi_hand_landmarks:
#         if results.multi_handedness:
#             hand_type = results.multi_handedness[0].classification[0].label
#
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(imgRGB, hand_landmarks,
#                                       mp_hands.HAND_CONNECTIONS,
#                                       mp_drawing.DrawingSpec(
#                                           color=(0, 0, 255)),
#                                       mp_drawing.DrawingSpec(
#                                           color=(0, 0, 0)))
#
#         for id, lm in enumerate(hand_landmarks.landmark):
#             h, w, c = frame.shape
#             cx, cy = int(lm.x * w), int(lm.y * h)
#             cords[f"{id}"] = cx, cy
#
#         if len(cords) == 21:
#             if hand_type == "Right":
#                 if int(cords['8'][1]) > int(cords['6'][1]) \
#                         and int(cords['12'][1]) > int(cords['10'][1]) \
#                         and int(cords['16'][1]) > int(cords['14'][1]) \
#                         and int(cords['20'][1]) > int(cords['18'][1]) \
#                         and int(cords['4'][0]) > int(cords['2'][0]):
#                     last_status = "Close"
#                 else:
#                     last_status = "Open"
#
#             elif hand_type == "Left":
#                 if int(cords['8'][1]) > int(cords['6'][1]) \
#                         and int(cords['12'][1]) > int(cords['10'][1]) \
#                         and int(cords['16'][1]) > int(cords['14'][1]) \
#                         and int(cords['20'][1]) > int(cords['18'][1]) \
#                         and int(cords['4'][0]) < int(cords['2'][0]):
#                     last_status = "Close"
#                 else:
#                     last_status = "Open"
#
#     else:
#         hand_type = "-"
#         last_status = "-"
#
#     return hand_type, last_status
