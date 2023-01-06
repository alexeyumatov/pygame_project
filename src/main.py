import pygame
from player_config import Player
import mediapipe as mp
import cv2
from pygame.math import Vector2
from groups import all_sprites, tiles_group, walls_group, ladder_group, floor_group
from functions import load_image, load_level, display_buttons
from location import draw_location
from camera import Camera, camera_func
from menu import start_screen
from level_choose import level_choose
from options import options_screen
from config import *

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

button_x_size, button_y_size, font = buttons(350, 70, 35)


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


pause_background = load_image('pause/Pause.png')


def draw_window():
    screen.fill(level_color)
    for el in all_sprites:
        screen.blit(el.image, camera.apply(el))
    pygame.display.flip()


def draw_pause():
    button_collides = []
    button_texts = []
    width, height = resolution
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


def pause():
    paused = True
    button_collides, button_texts = draw_pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "resume":
                            paused = False
                            return text
                        elif text == "options":
                            settings = options_screen()
                            if settings == 'back':
                                paused = False
                                draw_window()
                                pause()

                        elif text == "exit":
                            pygame.quit()
                            quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        # pygame.display.update()
        clock.tick(MENU_FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN)
    doing = start_screen()
    while doing != "play":
        if doing == "options":
            settings = options_screen()
            if settings == 'back':
                doing = start_screen()
    if doing == "play":
        level = level_choose()
    level_x, level_y = draw_location(load_level(f'levels/level_{level}.txt'))
    left, right = False, False
    left_stop, right_stop = False, False
    up, down = False, False
    up_stop, down_stop = False, False
    onGround = False

    camera = Camera(camera_func, 3840, 3072)
    hero = Player()

    # cap = cv2.VideoCapture(0)
    # w, h = 640, 480
    # cap.set(3, w)
    # cap.set(4, h)

    running = True
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN:
                    hero.shoot()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        doing = pause()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        left_stop, right_stop = False, False
                        left = True
                        right = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        left_stop, right_stop = False, False
                        right = True
                        left = False

                    if event.key == pygame.K_e and not hero.onLadder:
                        hero.ladder_climb(ladder_group, floor_group)
                    elif event.key == pygame.K_e and hero.onLadder:
                        hero.onLadder = False
                        up, down, up_stop, down_stop = False, False, False, False

                    if hero.onLadder:
                        if event.key == pygame.K_w:
                            if down:
                                pass
                            else:
                                up, down = True, False
                                up_stop, down_stop = False, False
                        elif event.key == pygame.K_s:
                            if up:
                                pass
                            else:
                                up, down = False, True
                                up_stop, down_stop = False, False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if right is False:
                            left_stop = True
                            hero.velx = 15
                        left = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if left is False:
                            right_stop = True
                            hero.velx = 15
                        right = False
                    if hero.onLadder:
                        if event.key == pygame.K_w:
                            up, down = False, False
                            up_stop, down_stop = True, False
                        elif event.key == pygame.K_s:
                            up, down = False, False
                            up_stop, down_stop = False, True

            hero.collider(walls_group)
            if hero.onLadder:
                if not hero.ladder_climb(ladder_group, floor_group):
                    up, down, up_stop, down_stop = False, False, False, False
                hero.acceleration(left, right, up, down)
                hero.stop(left_stop, right_stop, up_stop, down_stop)
                hero.bullet_update()
            else:
                hero.update(floor_group)
                hero.acceleration(left, right)
                hero.stop(left_stop, right_stop)
                hero.bullet_update()

            camera.update(hero)
            draw_window()

            clock.tick(FPS)
    pygame.quit()
