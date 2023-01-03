import pygame
from load_funcs import load_level
from Location import draw_location
from groups import all_sprites

if __name__ == '__main__':
    pygame.init()
    level_x, level_y = draw_location(load_level('levels/level_1.txt'))
    size = width, height = 3840, 3072
    screen = pygame.display.set_mode(size, pygame.SCALED | pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 30, 38))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
