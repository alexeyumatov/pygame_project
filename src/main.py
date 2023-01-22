from menu import start_screen, pause
import mediapipe as mp
import cv2
from groups import ladder_group, floor_group, enemies_group, player_group, enemy_bullets
from functions import load_image, draw_window, display_player_data
from level_choose_screen import level_choose
from db_functions import levels_amount_update, levels_amount_select, shield_points_select
from config import *


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

pause_background = load_image('pause/Pause.png')
screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN, vsync=1)


def main():
    level_number = start_screen()

    pygame.init()

    # cap = cv2.VideoCapture(0)
    # w, h = 640, 480
    # cap.set(3, w)
    # cap.set(4, h)

    running = True
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
        while running:
            for el in player_group:
                hero = el
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    hero.shoot()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()
                        pass
                    if event.key == pygame.K_e and not hero.onLadder:
                        hero.ladder_climb(ladder_group, floor_group)
                    elif event.key == pygame.K_e and hero.onLadder:
                        hero.onLadder = False

            if hero.update():
                if levels_amount_select(1) == level_number:
                    levels_amount_update(1)
                level_number = level_choose()
            hero.bullet_update()
            enemies_group.update()
            enemy_bullets.update()

            if hero.onLadder:
                hero.ladder_climb(ladder_group, floor_group)

            camera.update(hero)
            draw_window()

            display_player_data(hero.health_points, hero.shield_points)

            pygame.display.flip()
            if hero.is_killed:
                main()

            clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
