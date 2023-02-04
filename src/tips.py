from config import *


pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)


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
