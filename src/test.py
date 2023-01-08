import pygame
import sys
from config import clock, FPS


def scrollY(screenSurf, bg, bg_rect, offsetY):
    bg_rect[1] += offsetY
    if abs(bg_rect[1]) >= 2100:
        bg_rect[1] = -2100
    if bg_rect[1] > 0:
        bg_rect[1] = 0
    screenSurf.blit(bg, bg_rect)


def main():

    pygame.init()

    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

    bg = pygame.image.load("data/Menu/level_choose/level_choose.png")
    bg_rect = bg.get_rect()
    bg_rect[1] = -2100
    screen.blit(bg, bg_rect)

    pygame.display.update()

    while True:  # <-- the pyGame loop

        event = pygame.event.poll()
        pressed = pygame.key.get_pressed()

        # handle window closing
        if event.type == pygame.QUIT:
            break

        # handle scrolling
        if pressed[pygame.K_UP]:
            scrollY(screen, bg, bg_rect, 30)
        elif pressed[pygame.K_DOWN]:
            scrollY(screen, bg, bg_rect, -30)
        elif pressed[pygame.K_q]:
            break

        # updates what the window displays
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    # runs the pyGame loop
    main()
