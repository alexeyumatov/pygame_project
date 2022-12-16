import pygame
import os
import sys

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    image = load_image('hero/hero_idle.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 200
        self.rect.y = 200
        self.velx = 10
        self.vely = 0

    def update(self, left, right, up):
        if left:
            self.rect = self.rect.move(-self.velx, 0)
        elif right:
            self.rect = self.rect.move(self.velx, 0)


all_sprites = pygame.sprite.Group()
