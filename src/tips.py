from config import *


pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)


def market_tip():
    tip = data_font.render('Press Backspace to return to the level selection screen', True, white)
    screen.blit(tip, (540, 1024))


def settings_tip():
    tip = data_font.render('Press Backspace to return', True, white)
    screen.blit(tip, (773, 1024))


def level_choose_tip():
    tip = data_font.render('Use Arrow Up or Arrow Down to navigate through the level selection pages', True, white)
    screen.blit(tip, (390, 1024))


def ultimate_tip():
    tip = data_font.render('Press Z to activate ultimate attack', True, white)
    screen.blit(tip, (710, 40))


def fountain_tip():
    tip = data_font.render('Press Q to activate the fountain (wait 2 seconds)', True, white)
    screen.blit(tip, (600, 40))


def ladder_stick_tip():
    tip = data_font.render('Press E to attach to the ladder', True, white)
    screen.blit(tip, (715, 40))


def ladder_stop_tip():
    tip = data_font.render('Press E to detach from the ladder', True, white)
    screen.blit(tip, (710, 40))


def ultimate_waiting_tip():
    tip = data_font.render('Wait 2 seconds', True, white)
    screen.blit(tip, (835, 40))


def restart_game_tip():
    tip = data_font.render('Restart the game to apply the changes', True, white)
    screen.blit(tip, (680, 960))
