import pygame
from player_config import all_sprites, Player
import mediapipe as mp
import cv2


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    left, right, up = False, False, False

    hero = Player()

    last_status, hand_type = "", ""
    cap = cv2.VideoCapture(0)
    w, h = 640, 480
    cap.set(3, w)
    cap.set(4, h)
    cords = {}

    running = True
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
        while running:
            clock.tick(FPS)

            success, frame = cap.read()
            frame = cv2.flip(frame, 1)

            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                if results.multi_handedness:
                    hand_type = results.multi_handedness[0].classification[0].label

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(imgRGB, hand_landmarks,
                                              mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(
                                                  color=(0, 0, 255)),
                                              mp_drawing.DrawingSpec(
                                                  color=(0, 0, 0)))

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cords[f"{id}"] = cx, cy

                if len(cords) == 21:
                    if hand_type == "Right":
                        if int(cords['8'][1]) > int(cords['6'][1]) \
                                and int(cords['12'][1]) > int(cords['10'][1]) \
                                and int(cords['16'][1]) > int(cords['14'][1]) \
                                and int(cords['20'][1]) > int(cords['18'][1]) \
                                and int(cords['4'][0]) > int(cords['2'][0]):
                            last_status = "Close"
                        else:
                            last_status = "Open"

                    elif hand_type == "Left":
                        if int(cords['8'][1]) > int(cords['6'][1]) \
                                and int(cords['12'][1]) > int(cords['10'][1]) \
                                and int(cords['16'][1]) > int(cords['14'][1]) \
                                and int(cords['20'][1]) > int(cords['18'][1]) \
                                and int(cords['4'][0]) < int(cords['2'][0]):
                            last_status = "Close"
                        else:
                            last_status = "Open"

            else:
                hand_type = "-"
                last_status = "-"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(last_status, hand_type)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    left = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    right = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    up = True
                if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    left = False
                if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    right = False
                if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    up = False

            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            hero.update(left, right, up)
            pygame.display.flip()
    pygame.quit()
