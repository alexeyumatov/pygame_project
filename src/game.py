import asyncio

import pygame.display

from src.menu import start_screen, pause, death_screen
from src.groups import *
from src.functions import load_image, draw_window, display_player_data
from src.tips import *
from src.level_choose_screen import level_choose
from src.db_functions import levels_amount_update, levels_amount_select, \
    stamina_update, stamina_select, tips_select
from src.config import *

pause_background = load_image('pause/Pause.png')
screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN,
                                 vsync=1)
ultimate_attack, ultimate_attack_is_able = False, False


async def hands_detection():
    global last_status
    if hands_detect:
        with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9,
                            min_detection_confidence=0.9) as hands:
            while True:
                # LOAD CAMERA
                success, frame = cap.read()
                frame = cv2.flip(frame, 1)
                # GET IMAGE FROM CAMERA
                imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(imgRGB)
                imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    if results.multi_handedness:
                        # DETERMINE HAND (LEFT OR RIGHT)
                        hand_type = \
                            results.multi_handedness[0].classification[0].label

                    for hand_landmarks in results.multi_hand_landmarks:
                        # BUILDING A SKELETON OF A HAND
                        mp_drawing.draw_landmarks(imgRGB, hand_landmarks,
                                                  mp_hands.HAND_CONNECTIONS,
                                                  mp_drawing.DrawingSpec(
                                                      color=(0, 0, 255)),
                                                  mp_drawing.DrawingSpec(
                                                      color=(0, 0, 0)))

                    for id, lm in enumerate(hand_landmarks.landmark):
                        # GET THE COORDINATES OF THE HAND SECTIONS
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cords[f"{id}"] = cx, cy

                    if len(cords) == 21:  # CHECKING IF ALL COORDINATES
                        # ARE FOUND

                        # DETERMINE THE STATE OF THE HAND BY THE COORDINATES
                        if hand_type == "Right":
                            if int(cords['8'][1]) > int(cords['6'][1]) \
                                    and \
                                    int(cords['12'][1]) > int(cords['10'][1]) \
                                    and \
                                    int(cords['16'][1]) > int(cords['14'][1]) \
                                    and \
                                    int(cords['20'][1]) > int(cords['18'][1]) \
                                    and \
                                    int(cords['4'][0]) > int(cords['2'][0]):
                                last_status = "Close"
                            else:
                                last_status = "Open"

                        elif hand_type == "Left":
                            if int(cords['8'][1]) > int(cords['6'][1]) \
                                    and \
                                    int(cords['12'][1]) > int(cords['10'][1]) \
                                    and \
                                    int(cords['16'][1]) > int(cords['14'][1]) \
                                    and \
                                    int(cords['20'][1]) > int(cords['18'][1]) \
                                    and \
                                    int(cords['4'][0]) < int(cords['2'][0]):
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
    last_status = '-'

    running = True
    health_tip = False  # True if fountain tip is on screen
    ult_tip = False
    ultimate_timer = 0  # Activates if hands detection is off
    while running:
        for el in player_group:
            hero = el
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                    and not hero.onLadder and not hero.death_anim:
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
                if event.key == pygame.K_LSHIFT and not hero.onLadder and hero.dash_cooldown > 60:
                    hero.dash = True
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

        if hero.update():
            if levels_amount_select(1) == level_number:
                levels_amount_update(1)
            level_number = level_choose()
        enemies_group.update()
        enemy_bullets.update()
        hero.bullet_update()
        fountain_group.update()
        thorn_group.update()
        hostile_block_group.update()

        if hero.onLadder:
            hero.ladder_climb(ladder_group, floor_group)

        camera.update(hero)
        draw_window()

        if ultimate_attack_is_able:
            if last_status == 'Close' and hands_detect:
                hero.ultimate()
                stamina_update(1, -100)
                hero.stamina = stamina_select(1)
                last_status = '-'
                ultimate_attack_is_able = False
                ultimate_attack = False
            elif not hands_detect:
                if tips_select():
                    ultimate_waiting_tip()
                ultimate_timer += 1
                if ultimate_timer >= 120:
                    hero.ultimate()
                    stamina_update(1, -100)
                    hero.stamina = stamina_select(1)
                    ultimate_timer = 0
                    ultimate_attack_is_able = False
                    ultimate_attack = False

        # SHOWS THE ULTIMATE TIP
        if ultimate_attack and not ultimate_attack_is_able and not health_tip:
            if tips_select():
                ultimate_tip()
                ult_tip = True
        else:
            ult_tip = False

        if hero.ladder_hit and not hero.onLadder and not ult_tip:
            if tips_select():
                ladder_stick_tip()
        if hero.onLadder and not ult_tip:
            if tips_select():
                ladder_stop_tip()

        # SHOWS THE FOUNTAIN TIP AND PLAYER DATA
        # (2 types of hearts: is poisoned, not poisoned)
        if hero.isPoisoned:
            if hero.able_to_heal:
                if tips_select():
                    fountain_tip()
                    health_tip = True
            else:
                health_tip = False
            display_player_data(hero, ultimate_attack_is_able, True, False if hero.dash_cooldown <= 60 else True)
        else:
            display_player_data(hero, ultimate_attack_is_able, False, False if hero.dash_cooldown <= 60 else True)

        pygame.display.flip()
        if hero.is_killed:
            death_screen()

        # ASYNCHRONY WITH HANDS DETECTION
        if ultimate_attack_is_able and hands_detect:
            await asyncio.sleep(0)

        clock.tick(FPS)
    pygame.quit()
