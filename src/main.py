import mediapipe as mp
import cv2
from groups import ladder_group, floor_group
from functions import load_image, load_level, draw_window
from location import draw_location
from menu import start_screen, pause
from level_choose import level_choose
from options import options_screen
from player_config import Player
from config import *

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

pause_background = load_image('pause/Pause.png')


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
                        pause()
                        pass
                    if event.key == pygame.K_e and not hero.onLadder:
                        hero.ladder_climb(ladder_group, floor_group)
                    elif event.key == pygame.K_e and hero.onLadder:
                        hero.onLadder = False

            hero.update()
            hero.bullet_update()

            if hero.onLadder:
                hero.ladder_climb(ladder_group, floor_group)

            camera.update(hero)
            draw_window()

            clock.tick(FPS)
    pygame.quit()
