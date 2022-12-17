import pygame
from load_image import load_image
from groups import all_sprites, floor_group

g = 10


class Player(pygame.sprite.Sprite):
    image = load_image('hero/hero_idle.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 200
        self.y = 150
        self.rect.y = self.y
        self.velx = 0
        self.vely = 0
        self.phase = 0

    def update(self, collide_group):
        elem = [el for el in collide_group][0]
        if not pygame.sprite.collide_mask(self, elem):
            self.phase = 2
        if self.phase == 0:
            self.vely = 0
            self.rect.y = self.y
        elif self.phase > 0:
            self.phase -= 2
            self.vely += g / 30
            self.rect.y += 30 * self.vely / 20
            self.y += 30 * self.vely / 20

    def acceleration(self, left, right):
        if left:
            if self.velx < 15:
                self.velx += 2
            self.rect = self.rect.move(-self.velx, 0)
        elif right:
            if self.velx < 15:
                self.velx += 2
            self.rect = self.rect.move(self.velx, 0)

    def stop(self, left, right):
        if left:
            if self.velx > 0:
                self.velx -= 2
            else:
                self.velx = 0
            self.rect = self.rect.move(-self.velx, 0)
        elif right:
            if self.velx > 0:
                self.velx -= 2
            else:
                self.velx = 0
            self.rect = self.rect.move(self.velx, 0)
