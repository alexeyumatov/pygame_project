import pygame
import sys

pygame.init()

# SCREEN CONST
res = (1920, 1080)
screen = pygame.display.set_mode(res)
screen.fill((0, 30, 38))
width = screen.get_width()
height = screen.get_height()

# COLORS
white_color = (255, 255, 255)
light_color = (170, 170, 170)
dark_color = (0, 0, 0)

# BUTTON CONST
font = pygame.font.Font('data/Font/Main_Font.ttf', 65)
button_x_size = 140
button_y_size = 140
button_collides = []
button_texts = []


def display_buttons(button_rect, button_text, button_x_pos, button_y_pos):
    pygame.draw.rect(screen, white_color, button_rect)
    screen.blit(button_text, (button_x_pos - 15, button_y_pos - 45))


def level_choose():
    for i in range(9):
        button_x_pos = width / 9 + i * 160
        button_y_pos = width / 9
        button_rect = pygame.Rect(button_x_pos, button_y_pos, 0, 0).inflate(button_x_size, button_y_size)
        button_text = font.render(f'{i + 1}', True, dark_color)
        display_buttons(button_rect, button_text, button_x_pos, button_y_pos)
        button_collides.append(button_rect)
        button_texts.append(i + 1)
        pygame.display.update()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)
                    if collide:
                        level_number = button_texts[button_collides.index(elem)]
                        return level_number
        pygame.display.update()


