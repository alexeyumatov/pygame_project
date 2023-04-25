import pygame
import sys
import os
import multiprocessing
from ctypes import c_wchar_p
from src.game import game_func
from src.functions import load_image

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    # os.environ['SDL_VIDEODRIVER'] = 'dummy'
    icon = load_image('icon/dark_light_icon.png')
    pygame.display.set_caption('Dark Light', 'Dark Light')
    pygame.display.set_icon(icon)
    manager = multiprocessing.Manager()
    last_st = manager.Value(c_wchar_p, '-')
    stop_ev = multiprocessing.Event()
    task1 = multiprocessing.Process(target=game_func, args=(last_st, stop_ev))
    task1.start()
    task1.join()
