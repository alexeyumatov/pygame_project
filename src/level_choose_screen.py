import sys

import pygame.key

from config import *
from functions import scroll_function, load_image, load_level, game_melody, market_melody, main_melody
from location import draw_location
from groups import all_sprites, player_group, enemies_group
from db_functions import *
from tips import market_tip, level_choose_tip

pygame.init()

screen = screen_initialize()

bg = pygame.image.load("data/Menu/level_choose/level_choose.png")
bg_rect = bg.get_rect()

width = bg.get_width()
height = bg.get_height()

market_rect = pygame.Rect((879, 495, 620, 490))
market = pygame.Surface((620, 490))
market.fill(white)
market.set_alpha(0)

button_x_size, button_y_size, font = buttons(140, 140, 65)

levels_amount = levels_amount_select(1)


def display_buttons(button_image, button_rect):
    screen.blit(button_image, button_rect)


def level_choose():
    scroll_amount = -950
    bg_rect[1] = -6450
    screen.blit(bg, bg_rect)

    button_images = [load_image(f"Menu/buttons/numbered_buttons/"
                                f"level_button_{i}.png") for i in range(1, 15)]
    button_images.append(load_image("Menu/buttons/locked_level_button.png"))
    button_x_pos = 376
    phase = 0
    levels_amount = levels_amount_select(1)
    button_texts = [i for i in range(1, levels_amount + 1)]
    if len(button_texts) < 14:
        locked_levels = 14 - levels_amount
        for i in range(locked_levels):
            button_texts.append(0)

    while True:
        button_collides = []
        btn = []

        if phase != 7:
            if phase == 0:
                level_choose_tip()
                screen.blit(market, market_rect)

            btn = button_texts[phase * 2:phase * 2 + 2]

            for i in range(2):
                if btn[i] > 0:
                    button_image = button_images[btn[i] - 1]
                else:
                    button_image = button_images[-1]
                button_rect = button_image.get_rect()
                if phase < 2:
                    button_y_pos = [540, 80]
                elif phase == 4 or phase == 5:
                    button_y_pos = [595, 155]
                else:
                    button_y_pos = [570, 115]
                button_rect.x, button_rect.y = button_x_pos, button_y_pos[i]
                display_buttons(button_image, button_rect)
                if btn[i] > 0:
                    button_collides.append(button_rect)

        pygame.display.update()

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for elem in button_collides:
                collide = elem.collidepoint(mouse_pos)
                if collide:
                    level_number = btn[button_collides.index(elem)]
                    for el in all_sprites:
                        el.kill()
                    for el in player_group:
                        el.kill()
                    for el in enemies_group:
                        el.kill()
                    if level_number < levels_amount:
                        coins = False
                    else:
                        coins = True
                    draw_location(load_level(f'levels/'
                                             f'level_{level_number}.txt'),
                                  coins)
                    game_melody()
                    return level_number
            market_coolide = market_rect.collidepoint(mouse_pos)
            if market_coolide and phase == 0:
                pygame.mixer.music.stop()
                return market_window()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if phase < 7:
                    if phase == 6:
                        scroll_amount -= 100
                    elif phase > 0:
                        scroll_amount += 15
                    phase += 1
                    scroll_function(screen, bg, bg_rect, abs(scroll_amount))
            elif event.key == pygame.K_DOWN:
                if phase > 0:
                    phase -= 1
                    scroll_function(screen, bg, bg_rect, scroll_amount)
                    if phase == 1 or phase == 0:
                        scroll_amount = -950
                    elif phase == 6:
                        scroll_amount += 100
                    else:
                        scroll_amount -= 15

            if event.key == pygame.K_i:
                sys.exit()

        clock.tick(MENU_FPS)


def market_window():
    screen.fill((0, 30, 38))
    market_melody()
    coins_amount = coins_select(1)

    # TEXTS FOR LOTS IN THE MARKET
    texts = [f'Already Purchased: {shield_points_select(1)}',
             f'Delay now: {bullet_cooldown_select(1)[1]} ms',
             f'Already Purchased: {bullets_damage_select(1)}',
             f'Already Purchased: '
             f'{"Yes" if bullet_is_collidable_select(1) else "No"}']

    lots_rect = [pygame.Rect(80, 300, 270, 270), pygame.Rect(580, 300,
                                                             270, 270),
                 pygame.Rect(1080, 300, 270, 270), pygame.Rect(1580, 300,
                                                               270, 270)]
    lots = [load_image('Menu/market/armor_upgrade.png', -1),
            load_image('Menu/market/bullet_cooldown_upgrade.png', -1),
            load_image('Menu/market/bullet_damage_upgrade.png', -1),
            load_image('Menu/market/bullets_collide_upgrade.png', -1)]
    lots_texts = ['Shield Upgrade', 'Bullets Amount', 'Bullets Damage',
                  'Collision of Bullets']

    purchase_buttons_rect = [pygame.Rect(80, 700, 270, 60),
                             pygame.Rect(580, 700, 270, 60),
                             pygame.Rect(1080, 700, 270, 60),
                             pygame.Rect(1580, 700, 270, 60)]
    purchase_buttons = [load_image('Menu/market/market_buttons'
                                   '/available/shield_points.png'),
                        load_image('Menu/market/market_buttons'
                                   '/available/bullets_amount.png'),
                        load_image('Menu/market/market_buttons'
                                   '/available/bullets_damage.png'),
                        load_image('Menu/market/market_buttons'
                                   '/available/bullets_collide.png')]

    blocked_buttons = [load_image('Menu/market/market_buttons/'
                                  'not_enough_coins/shield_points.png'),
                       load_image('Menu/market/market_buttons/'
                                  'not_enough_coins/bullets_amount.png'),
                       load_image('Menu/market/market_buttons/'
                                  'not_enough_coins/bullets_damage.png'),
                       load_image('Menu/market/market_buttons/'
                                  'not_enough_coins/bullets_collide.png')]

    max_buttons = [load_image('Menu/market/market_buttons/'
                              'maximum/max_amount.png')
                   for _ in range(len(purchase_buttons_rect))]

    prices = [10, 5, 15, 40]
    data = [shield_points_select(1), bullet_cooldown_select(1)[0],
            bullets_damage_select(1),
            bullet_is_collidable_select(1)]
    max_values = [50, 3, 30, 1]
    available_buttons = []

    # COINS COUNTER
    coin = load_image('objects/coin/coin.png', -1)
    coin = pygame.transform.scale(coin, (30, 45))

    # TIP AND HEADER
    market_tip()
    header = header_font.render('MARKET', True, white)
    screen.blit(header, (830, 48))

    while True:
        event = pygame.event.poll()

        for el in purchase_buttons_rect:
            index = purchase_buttons_rect.index(el)
            if prices[index] <= coins_amount and \
                    data[index] < max_values[index]:
                available_buttons.append(el)

        # COIN DATA
        coin_data = big_data_font.render(str(coins_amount), True, white)
        if coins_amount > 10:
            screen.blit(coin_data, (1700, 58))
        else:
            screen.blit(coin_data, (1720, 58))
        screen.blit(coin, (1770, 60))

        # MAIN INFORMATION
        for el in lots:
            index = lots.index(el)
            elem_data = market_font.render(texts[index], True, white)
            elem_name = big_market_font.render(lots_texts[index], True, white)
            lot_rect = lots_rect[index]
            if el == lots[-1]:
                screen.blit(elem_name, (lot_rect.x - 8, lot_rect.y - 64))
                screen.blit(elem_data, (lot_rect.x - 10, lot_rect.y + 300))
            elif el == lots[1]:
                screen.blit(elem_name, (lot_rect.x + 16, lot_rect.y - 64))
                screen.blit(elem_data, (lot_rect.x + 30, lot_rect.y + 300))
            else:
                screen.blit(elem_name, (lot_rect.x + 16, lot_rect.y - 64))
                screen.blit(elem_data, (lot_rect.x - 2, lot_rect.y + 300))
            screen.blit(el, lot_rect)

            if data[index] == max_values[index]:
                screen.blit(max_buttons[index],
                            purchase_buttons_rect[index])
            elif prices[index] <= coins_amount:
                screen.blit(purchase_buttons[index],
                            purchase_buttons_rect[index])
            else:
                screen.blit(blocked_buttons[index],
                            purchase_buttons_rect[index])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for el in available_buttons:
                collide = el.collidepoint(mouse_pos)
                if collide:
                    lot = purchase_buttons_rect.index(el)
                    if lot == 0:
                        shield_points_update(1)
                    elif lot == 1:
                        bullet_cooldown_update(1)
                    elif lot == 2:
                        bullets_damage_update(1)
                    elif lot == 3:
                        bullet_is_collided_update(1)
                    coins_update(1, -prices[lot])
                texts = [f'Already Purchased: {shield_points_select(1)}',
                         f'Delay now: {bullet_cooldown_select(1)[1]} ms',
                         f'Already Purchased: {bullets_damage_select(1)}',
                         f'Already Purchased: '
                         f'{"Yes" if bullet_is_collidable_select(1) else "No"}']
                coins_amount = coins_select(1)
                data = [shield_points_select(1), bullet_cooldown_select(1)[0],
                        bullets_damage_select(1),
                        bullet_is_collidable_select(1)]

        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            main_melody()
            return level_choose()

        pygame.display.update()
        available_buttons.clear()
        clock.tick(MENU_FPS)
