import src.config
import pygame
import multiprocessing

if __name__ == '__main__':
    pygame.init()
    src.config.screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN,
                                                vsync=1)
    multiprocessing.freeze_support()
    from ctypes import c_wchar_p
    from src.game import game_func
    from src.functions import load_image

    icon = load_image('icon/dark_light_icon.png')
    pygame.display.set_caption('Dark Light', 'Dark Light')
    pygame.display.set_icon(icon)
    manager = multiprocessing.Manager()
    last_st = manager.Value(c_wchar_p, '-')
    stop_ev = multiprocessing.Event()
    task1 = multiprocessing.Process(target=game_func, args=(last_st, stop_ev))
    task1.start()
    task1.join()
