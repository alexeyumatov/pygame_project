import pygame
import sys

pygame.init()
# SCREEN CONST
res = (1920, 1080)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()


# COLORS
white_color = (255, 255, 255)
light_color = (170, 170, 170)
dark_color = (0, 0, 0)

# BUTTON CONST
font = pygame.font.Font('data/Font/Main_Font.ttf', 35)
button_x_size = 350
button_y_size = 70
button_collides = []
button_texts = []


def display_buttons(button_rect, button_text, button_x_pos, button_y_pos, text):
    pygame.draw.rect(screen, white_color, button_rect)
    if text == "options":
        screen.blit(button_text, (button_x_pos - 75, button_y_pos - 25))
    else:
        screen.blit(button_text, (button_x_pos - 40, button_y_pos - 25))


def start_screen():
    for i in range(3):
        button_x_pos = width / 2
        button_y_pos = width / (5 - i) + 50
        button_rect = pygame.Rect(button_x_pos,
                                  button_y_pos, 0, 0).inflate(button_x_size,
                                                              button_y_size)
        button_text = ''
        text = ''

        if i == 0:
            button_text = font.render('Play', True, dark_color)
            text = 'play'
        elif i == 1:
            button_text = font.render('Options', True, dark_color)
            text = 'options'
        elif i == 2:
            button_text = font.render('Exit', True, dark_color)
            text = 'exit'

        button_texts.append(text)
        button_collides.append(button_rect)

        display_buttons(button_rect, button_text, button_x_pos, button_y_pos,
                        text)
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
                        text = button_texts[button_collides.index(elem)]
                        if text == "play":
                            screen.fill((0, 30, 38))
                            return text
                        elif text == "options":
                            pass
                        elif text == "exit":
                            quit()

        pygame.display.update()
