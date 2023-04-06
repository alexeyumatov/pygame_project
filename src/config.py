import pygame
from src.camera import Camera, camera_func
import mediapipe as mp
import cv2
from src.db_functions import hands_detection_select


# SCREEN
resolution = (1920, 1080)
FPS = 60
MENU_FPS = 24


# SETTINGS
hands_detect = hands_detection_select()


# HANDS
if hands_detect:
    cords = {}
    last_status, hand_type = "-", ""
    cap = cv2.VideoCapture(0)
    w, h = 1280, 720
    cap.set(3, w)
    cap.set(4, h)


# CAMERA INITIALIZE
camera = Camera(camera_func, 3840, 3072)
pygame.init()


# HANDS
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# COLORS
level_color = (0, 30, 38)
white = (255, 255, 255)
light_gray = (170, 170, 170)
black = (0, 0, 0)
red = (230, 0, 0)


# IMAGES
width, height = 74, 64

heart = pygame.image.load('src/data/player_data/heart.png')
heart = pygame.transform.scale(heart, (width, height))
heart.set_alpha(210)

poisoned_heart = pygame.image.load('src/data/player_data/poisoned_heart.png')
poisoned_heart = pygame.transform.scale(poisoned_heart, (width, height))
poisoned_heart.set_alpha(210)

shield = pygame.image.load('src/data/player_data/shield.png')
shield = pygame.transform.scale(shield, (width, 64))
shield.set_alpha(210)

ultimate_not_ready = \
    pygame.image.load('src/data/player_data/ultimate_attack/'
                      'ultimate_not_ready.png')
ultimate_not_ready = pygame.transform.scale(ultimate_not_ready, (90, 90))
ultimate_not_ready.set_alpha(210)

ultimate_ready = \
    pygame.image.load('src/data/player_data/ultimate_attack/ultimate_ready.png')
ultimate_ready = pygame.transform.scale(ultimate_ready, (90, 90))
ultimate_ready.set_alpha(210)


# TEXT
data_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 24)
big_data_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 36)
market_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 20)
big_market_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 26)
header_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 60)
settings_font = pygame.font.Font('src/data/Font/Main_Font.ttf', 38)


# TIME
clock = pygame.time.Clock()


# BUTTONS
def buttons(x_size, y_size, font_size):
    return x_size, y_size, pygame.font.Font('src/data/Font/'
                                            'Main_Font.ttf', font_size)


def screen_initialize():
    screen = \
        pygame.display.set_mode(resolution, pygame.SCALED | pygame.FULLSCREEN)
    screen.fill(level_color)
    return screen
