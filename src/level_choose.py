import pygame
from config import *

pygame.init()

screen = screen_initialize()
width = screen.get_width()
height = screen.get_height()

button_x_size, button_y_size, font = buttons(140, 140, 65)


def display_buttons(button_rect, button_text, button_x_pos, button_y_pos):
    pygame.draw.rect(screen, white, button_rect)
    screen.blit(button_text, (button_x_pos - 15, button_y_pos - 45))


def level_choose():
    button_collides = []
    button_texts = []

    for i in range(9):
        button_x_pos = width / 9 + i * 160
        button_y_pos = width / 9
        button_rect = pygame.Rect(button_x_pos, button_y_pos, 0, 0).inflate(button_x_size, button_y_size)
        button_text = font.render(f'{i + 1}', True, black)
        display_buttons(button_rect, button_text, button_x_pos, button_y_pos)
        button_collides.append(button_rect)
        button_texts.append(i + 1)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)
                    if collide:
                        level_number = button_texts[button_collides.index(elem)]
                        return level_number

        clock.tick(MENU_FPS)


