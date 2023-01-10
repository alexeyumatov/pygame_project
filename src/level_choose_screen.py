import pygame.key

from config import *
from functions import scroll_function

pygame.init()

screen = screen_initialize()

bg = pygame.image.load("data/Menu/level_choose/level_choose.png")
bg_rect = bg.get_rect()
bg_rect[1] = -2100

width = bg.get_width()
height = bg.get_height()

button_x_size, button_y_size, font = buttons(140, 140, 65)


def display_buttons(button_rect, button_text, button_x_pos, button_y_pos):
    pygame.draw.rect(screen, white, button_rect)
    screen.blit(button_text, (button_x_pos - 15, button_y_pos - 45))


def level_choose():
    button_collides = []
    button_texts = []

    screen.blit(bg, bg_rect)

    for i in range(9):
        button_x_pos = 385
        button_y_pos = i * 180
        button_rect = pygame.Rect(button_x_pos, button_y_pos, 0, 0).inflate(button_x_size, button_y_size)
        button_text = font.render(f'{i + 1}', True, black)
        display_buttons(button_rect, button_text, button_x_pos, button_y_pos)
        button_collides.append(button_rect)
        button_texts.append(i + 1)

    pygame.display.update()

    while True:
        key = pygame.key.get_pressed()
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for elem in button_collides:
                collide = elem.collidepoint(mouse_pos)
                if collide:
                    level_number = button_texts[button_collides.index(elem)]
                    return level_number

        if key[pygame.K_UP]:
            scroll_function(screen, bg, bg_rect, 30)
        elif key[pygame.K_DOWN]:
            scroll_function(screen, bg, bg_rect, -30)
        # elif key[pygame.K_ESCAPE]:
        #     return 'back'

        pygame.display.update()

        clock.tick(FPS)
