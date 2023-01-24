from config import *
from functions import display_buttons, draw_pause, draw_window, load_image
from level_choose_screen import level_choose


pygame.init()

screen = pygame.display.set_mode(resolution)
width = screen.get_width()
height = screen.get_height()

screen.fill(level_color)

button_x_size, button_y_size, font = buttons(350, 70, 35)


def start_screen():
    screen.fill(level_color)
    button_collides = []
    button_texts = []
    animCount = 0
    background = [load_image(f'Menu/main_menu/{i}.png') for i in range(1, 9)]

    while True:
        if animCount + 1 >= 56:
            animCount = 0

        screen.blit(background[animCount // 7], (0, 0))
        animCount += 1

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

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "play":
                            screen.fill((0, 30, 38))
                            return level_choose()
                        elif text == "options":
                            screen.fill((0, 30, 38))
                            return options_screen(False)
                        elif text == "exit":
                            quit()

        pygame.display.update()
        clock.tick(FPS)


def pause():
    paused = True
    draw_window()
    button_collides, button_texts = draw_pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for elem in button_collides:
                    collide = elem.collidepoint(mouse_pos)

                    if collide:
                        text = button_texts[button_collides.index(elem)]
                        if text == "resume":
                            return text
                        elif text == "options":
                            return options_screen(True)
                        elif text == "exit":
                            return start_screen()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        clock.tick(MENU_FPS)


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
            button_text = font.render('Back', True, black)
            text = 'back'

        elif i == 1:
            button_text = font.render('Screen', True, black)
            text = 'screen'
        elif i == 2:
            button_text = font.render('Camera', True, black)
            text = 'camera'

        elif i == 3:
            button_text = font.render('Key Bindings', True, black)
            text = 'key bindings'

        button_texts.append(text)
        button_collides.append(button_rect)

        display_buttons(button_rect, button_text, button_x_pos, button_y_pos,
                        text)
        pygame.display.update()


def options_screen(from_pause):
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
                            if from_pause:
                                return pause()
                            else:
                                return start_screen()
                        elif text == 'screen':
                            pass
                        elif text == 'camera':
                            pass
                        elif text == 'key bindings':
                            pass

        pygame.display.update()
        clock.tick(MENU_FPS)
