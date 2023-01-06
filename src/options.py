import pygame
from functions import display_buttons

pygame.init()
# SCREEN CONST
res = (1920, 1080)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()
screen.fill((0, 30, 38))


# COLORS
light_color = (170, 170, 170)
dark_color = (0, 0, 0)

# BUTTON CONST
font = pygame.font.Font('data/Font/Main_Font.ttf', 35)
button_x_size = 350
button_y_size = 70
button_collides = []
button_texts = []


def selection_buttons():
    for i in range(4):
        button_x_pos = width / 7 + i * 450
        button_y_pos = width / 10 - 100
        button_rect = pygame.Rect(button_x_pos,
                                  button_y_pos, 0, 0).inflate(button_x_size,
                                                              button_y_size)
        button_text = ''
        text = ''

        if i == 0:
            button_text = font.render('Back', True, dark_color)
            text = 'back'

        elif i == 1:
            button_text = font.render('Screen', True, dark_color)
            text = 'screen'
        elif i == 2:
            button_text = font.render('Camera', True, dark_color)
            text = 'camera'

        elif i == 3:
            button_text = font.render('Key Bindings', True, dark_color)
            text = 'key bindings'

        button_texts.append(text)
        button_collides.append(button_rect)

        display_buttons(button_rect, button_text, button_x_pos, button_y_pos,
                        text)
        pygame.display.update()


def options_screen():
    screen.fill((0, 30, 38))
    selection_buttons()
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
                        if text == 'back':
                            return text
                        elif text == 'screen':
                            pass
                        elif text == 'camera':
                            pass
                        elif text == 'key bindings':
                            pass

        pygame.display.update()
