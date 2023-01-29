import asyncio

import pygame.display

from menu import start_screen, pause
from groups import ladder_group, floor_group, enemies_group, player_group, enemy_bullets, fountain_group
from functions import load_image, draw_window, display_player_data, ultimate_tip
from level_choose_screen import level_choose
from db_functions import levels_amount_update, levels_amount_select, stamina_update, stamina_select
from config import *


pause_background = load_image('pause/Pause.png')
screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN, vsync=1)
ultimate_attack, ultimate_attack_is_able = False, False


async def hands_detection():
    global last_status
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
        while True:
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
            await asyncio.sleep(0.5)


async def game_func():
    global ultimate_attack, last_status, ultimate_attack_is_able
    level_number = start_screen()

    pygame.init()

    running = True
    while running:
        for el in player_group:
            hero = el
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not hero.onLadder:
                hero.shoot()

            if event.type == pygame.KEYDOWN:
                if len(fountain_group) > 0:
                    for el in fountain_group:
                        fountain = el
                    if event.key == pygame.K_q and hero.able_to_heal:
                        fountain.isPressed = True
                    else:
                        fountain.isPressed = False
                if event.key == pygame.K_ESCAPE:
                    pause()
                    pass
                if event.key == pygame.K_e and not hero.onLadder:
                    hero.ladder_climb(ladder_group, floor_group)
                elif event.key == pygame.K_e and hero.onLadder:
                    hero.onLadder = False
                if ultimate_attack and event.key == pygame.K_z:
                    ultimate_attack = False
                    ultimate_attack_is_able = True
        if hero.stamina == 100:
            ultimate_attack = True
        else:
            ultimate_attack = False
        if last_status == 'Close' and ultimate_attack_is_able:
            hero.shoot()
            stamina_update(1, -100)
            hero.stamina = stamina_select(1)
            last_status = '-'
            ultimate_attack_is_able = False

        if hero.update():
            if levels_amount_select(1) == level_number:
                levels_amount_update(1)
            level_number = level_choose()
        enemies_group.update()
        enemy_bullets.update()
        hero.bullet_update()
        fountain_group.update()

        if hero.onLadder:
            hero.ladder_climb(ladder_group, floor_group)

        camera.update(hero)
        draw_window()

        if ultimate_attack and not ultimate_attack_is_able:
            ultimate_tip()

        if hero.isPoisoned:
            display_player_data(hero, ultimate_attack_is_able, True)
        else:
            display_player_data(hero, ultimate_attack_is_able)

        pygame.display.flip()
        if hero.is_killed:
            await game_func()

        if ultimate_attack_is_able:
            await asyncio.sleep(0)

        clock.tick(FPS)
    pygame.quit()


async def main():
    task1 = asyncio.create_task(game_func())
    task2 = asyncio.create_task(hands_detection())
    await task1
    await task2


if __name__ == '__main__':
    pygame.display.set_caption('Dark Light', 'Dark Light')
    icon = load_image('icon/dark_light_icon.png')
    pygame.display.set_icon(icon)
    asyncio.run(main())
