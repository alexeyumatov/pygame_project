import pygame
import sys


def scrollY(screenSurf, bg, offsetY):
    width, height = bg.get_size()
    screenSurf.blit(bg, (0, offsetY))
    if offsetY < 0:
        screenSurf.blit(bg, (0, height + offsetY), (0, 0, width, -offsetY))
    else:
        screenSurf.blit(bg, (0, 0), (0, height - offsetY, width, offsetY))


def main():

    pygame.init()

    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

    bg = pygame.image.load("level_choose.png").convert_alpha()

    while True:  # <-- the pyGame loop

        event = pygame.event.poll()
        pressed = pygame.key.get_pressed()

        # handle window closing
        if event.type == pygame.QUIT:
            break

        # handle scrolling
        if pressed[pygame.K_UP]:
            scrollY(screen, bg, 2)
        elif pressed[pygame.K_DOWN]:
            scrollY(screen, bg, -2)
        elif pressed[pygame.K_LEFT]:
            screen.scroll(2, 0)
        elif pressed[pygame.K_RIGHT]:
            screen.scroll(-2, 0)

        # updates what the window displays
        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    # runs the pyGame loop
    main()
