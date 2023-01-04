import pygame
from functions import load_image, flip


class Bullet(pygame.sprite.Sprite):
    bullet_images = [load_image(f'objects/bullet/{i}.png') for i in range(1, 7)]

    def __init__(self, x, y, player_view, collide_group, *groups):
        super().__init__(*groups)
        self.image = Bullet.bullet_images[0]
        self.image = pygame.transform.scale(self.image, (320, 320))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.collide_group = collide_group
        if player_view == "left":
            self.velx = -20
        elif player_view == "right":
            self.velx = 20
        self.view = player_view
        self.animCount = 0

    def update(self):
        self.rect.x += self.velx
        if self.animCount + 1 >= 42:
            self.animCount = 0
        self.image = Bullet.bullet_images[self.animCount // 7]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.view == "left":
            self.image = flip(self.image)
        self.animCount += 1

        if pygame.sprite.spritecollideany(self, self.collide_group):
            self.kill()
            return 'killed'
        else:
            return 'alive'
