import pygame
from player_config import all_sprites, Player
import mediapipe as mp
import cv2
from Location import Location
from groups import all_sprites, floor_group, left_walls, right_walls
from load_image import load_image

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


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

floor = Location('Locations/location_floor.png', all_sprites, floor_group)
left_wall = Location('Locations/location_left_wall.png', all_sprites,
                     left_walls)
right_wall = Location('Locations/location_right_wall.png', all_sprites,
                      right_walls)
ceiling = Location('Locations/location_ceiling.png', all_sprites)

paused = False


def draw_window():
    screen.fill((100, 100, 100))
    all_sprites.draw(screen)
    pygame.display.flip()


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.blit(pause_background, (0, 0))
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    left, right, up = False, False, False
    left_stop, right_stop = False, False
    onGround = False

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
                    pass

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()
                        pass
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if right:
                            pass
                        else:
                            left_stop, right_stop = False, False
                            right, left = False, True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if left:
                            pass
                        else:
                            left_stop, right_stop = False, False
                            right, left = True, False
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        hero.jump(floor_group)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        left_stop, right_stop = True, False
                        left, right = False, False
                        hero.velx = 15
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        left_stop, right_stop = False, True
                        left, right = False, False
                        hero.velx = 15
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        pass

            if not onGround:
                onGround = hero.fall(floor_group)
            else:
                hero.collider(left_walls, right_walls)
                hero.update(floor_group)
                hero.acceleration(left, right)
                hero.stop(left_stop, right_stop)

            draw_window()

            clock.tick(FPS)
    pygame.quit()
