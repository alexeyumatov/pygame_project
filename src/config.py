import pygame


# SCREEN
resolution = (1920, 1080)
FPS = 60
MENU_FPS = 24


# COLORS
level_color = (0, 30, 38)
white = (255, 255, 255)
light_gray = (170, 170, 170)
black = (0, 0, 0)


# TIME
clock = pygame.time.Clock()


# BUTTONS
def buttons(x_size, y_size, font_size):
    return x_size, y_size, pygame.font.Font('data/Font/Main_Font.ttf', font_size)


def screen_initialize():
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN)
    screen.fill(level_color)
    return screen
