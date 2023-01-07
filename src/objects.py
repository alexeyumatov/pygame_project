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
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect.x, self.rect.y = x, y
        self.count = 260
        self.collide_group = collide_group
        if player_view == "left":
            self.velx = -20
        elif player_view == "right":
            self.velx = 20
        self.view = player_view
        self.animCount = 0

    def update(self):
        if self.animCount + 1 >= 42:
            self.animCount = 0
        self.image = Bullet.bullet_images[self.animCount // 7]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.view == "left":
            self.image = flip(self.image)
        self.animCount += 1

        self.rect.x += self.velx

        if pygame.sprite.spritecollide(self, self.collide_group, False):
            if self.view == 'right':
                if self.count > 0:
                    self.count -= 20
                else:
                    self.kill()
                    return 'killed'
            else:
                self.kill()
                return 'killed'
        else:
            return 'alive'
