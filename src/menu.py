from functions import display_buttons
from config import *
from functions import draw_pause
from options import options_screen
from functions import draw_window

pygame.init()

screen = pygame.display.set_mode(resolution)
width = screen.get_width()
height = screen.get_height()

screen.fill(level_color)

button_x_size, button_y_size, font = buttons(350, 70, 35)


def start_screen():
    button_collides = []
    button_texts = []
    screen.fill((0, 30, 38))
    for i in range(3):
        button_x_pos = width / 2
        button_y_pos = width / (5 - i) + 50
        button_rect = pygame.Rect(button_x_pos,
                                  button_y_pos, 0, 0).inflate(button_x_size,
                                                              button_y_size)
        button_text = ''
        text = ''

        if i == 0:
            button_text = font.render('Play', True, black)
            text = 'play'
        elif i == 1:
            button_text = font.render('Options', True, black)
            text = 'options'
        elif i == 2:
            button_text = font.render('Exit', True, black)
            text = 'exit'

        button_texts.append(text)
        button_collides.append(button_rect)

        display_buttons(button_rect, button_text, button_x_pos, button_y_pos,
                        text)
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
                        text = button_texts[button_collides.index(elem)]
                        if text == "play":
                            screen.fill((0, 30, 38))
                            return text
                        elif text == "options":
                            screen.fill((0, 30, 38))
                            return text
                        elif text == "exit":
                            quit()

        clock.tick(MENU_FPS)


def pause():
    paused = True
    button_collides, button_texts = draw_pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "resume":
                            paused = False
                            return text
                        elif text == "options":

                            settings = options_screen()
                            if settings == 'back':
                                draw_window()
                                draw_pause()

                        elif text == "exit":
                            pygame.quit()
                            quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        # pygame.display.update()
        clock.tick(MENU_FPS)
