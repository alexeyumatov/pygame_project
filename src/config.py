import pygame
from camera import Camera, camera_func


# SCREEN
resolution = (1920, 1080)
FPS = 60
MENU_FPS = 24


# CAMERA INITIALIZE
camera = Camera(camera_func, 3840, 3072)
pygame.init()


# COLORS
level_color = (0, 30, 38)
white = (255, 255, 255)
light_gray = (170, 170, 170)
black = (0, 0, 0)


# IMAGES
heart = pygame.image.load('data/player_data/heart.png')
heart = pygame.transform.scale(heart, (74, 64))
heart.set_alpha(210)

shield = pygame.image.load('data/player_data/shield.png')
shield = pygame.transform.scale(shield, (74, 64))
shield.set_alpha(210)


# TEXT
data_font = pygame.font.Font('data/Font/Main_Font.ttf', 24)
market_font = pygame.font.Font('data/Font/Main_Font.ttf', 20)
big_market_font = pygame.font.Font('data/Font/Main_Font.ttf', 26)


# TIME
clock = pygame.time.Clock()


# BUTTONS
def buttons(x_size, y_size, font_size):
    return x_size, y_size, pygame.font.Font('data/Font/Main_Font.ttf', font_size)


def screen_initialize():
    screen = pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN)
    screen.fill(level_color)
    return screen
