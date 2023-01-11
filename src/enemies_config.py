import pygame
from functions import load_image, flip


class RegularEnemy(pygame.sprite.Sprite):
    images = [load_image(f'enemies/regular_enemy/{i}.png') for i in range(1, 9)]

    def __init__(self, x, y, *groups):
        super(RegularEnemy, self).__init__(*groups)
        self.image = RegularEnemy.images[0]
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.animCount = 0
        self.health_points = 30
        self.view = 'right'
        self.velx = 0
        self.distance = 0

    def update(self):
        vl_x = 0

        if self.animCount > 49:
            self.animCount = 0

        self.image = RegularEnemy.images[self.animCount // 7]
        if self.view == 'left':
            self.image = flip(self.image)
        self.animCount += 1

        if self.view == 'right':
            self.velx += 0.5
            if self.velx >= 8:
                self.velx = 8
            vl_x += self.velx
        elif self.view == 'left':
            self.velx -= 0.5
            if self.velx <= -8:
                self.velx = -8
            vl_x += self.velx

        self.distance += vl_x
        if abs(self.distance) >= 500:
            if self.view == 'right':
                self.view = 'left'
            else:
                self.view = 'right'
            self.distance = 0

        self.rect.x += vl_x

