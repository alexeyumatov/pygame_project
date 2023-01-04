import pygame
import sys


def start_screen():
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

    # PLAY BUTTON
    start_game_x_pos = width / 2
    start_game_y_pos = width / 5 + 50
    start_game_rect = pygame.Rect(start_game_x_pos, start_game_y_pos, 0, 0).inflate(button_x_size, button_y_size)
    start_game_text = font.render('Play', True, dark_color)

    # OPTIONS BUTTON
    options_x_pos = width / 2
    options_y_pos = width / 4 + 50
    options_rect = pygame.Rect(options_x_pos, options_y_pos, 0, 0).inflate(button_x_size, button_y_size)
    options_text = font.render('Options', True, dark_color)

    # EXIT BUTTON
    exit_game_x_pos = width / 2
    exit_game_y_pos = width / 3 + 50
    exit_game_rect = pygame.Rect(exit_game_x_pos, exit_game_y_pos, 0, 0).inflate(button_x_size, button_y_size)
    exit_game_text = font.render('Exit', True, dark_color)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # COLLIDE CHECK
        collide_start_game = start_game_rect.collidepoint(mouse_pos)
        collide_exit_game = exit_game_rect.collidepoint(mouse_pos)
        collide_options = options_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if collide_start_game:
                    screen.fill((0, 30, 38))
                    return "play"
                elif collide_options:
                    print("options")
                elif collide_exit_game:
                    quit()

        # DISPLAY BUTTONS
        screen.fill((0, 30, 38))
        pygame.draw.rect(screen, white_color, start_game_rect)
        screen.blit(start_game_text, (start_game_x_pos - 40, start_game_y_pos - 25))

        pygame.draw.rect(screen, white_color, options_rect)
        screen.blit(options_text, (options_x_pos - 75, options_y_pos - 25))

        pygame.draw.rect(screen, white_color, exit_game_rect)
        screen.blit(exit_game_text, (exit_game_x_pos - 40, exit_game_y_pos - 25))

        pygame.display.update()
