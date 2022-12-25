import pygame
from load_image import load_image
from groups import bullets


class Ladder(pygame.sprite.Sprite):
    image = load_image('objects/Ladder.png', -1)

    def __init__(self, *groups):
        super(Ladder, self).__init__(*groups)
        self.image = Ladder.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 500
        self.rect.y = 400


class Bullet(pygame.sprite.Sprite):
    bullet_images = [load_image(f'objects/bullet/{i}.png') for i in range(1, 31)]

    def __init__(self, x, y, *groups):
        super().__init__(bullets, *groups)
        self.image = Bullet.bullet_images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.velx = 10
        self.animCount = 0

    def update(self):
        self.rect.x += self.velx
        if self.animCount + 1 >= 60:
            self.animCount = 0
        self.image = Bullet.bullet_images[self.animCount // 2]
        self.animCount += 1
        print(self.rect.right)
        if self.rect.right > 1000:
            self.kill()
