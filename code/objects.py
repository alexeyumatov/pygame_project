import pygame
from load_image import load_image


class Ladder(pygame.sprite.Sprite):
    image = load_image('objects/Vertical_Ladder.png')

    def __init__(self, x, y, *groups):
        super(Ladder, self).__init__(*groups)
        self.image = Ladder.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    bullet_images = [load_image(f'objects/bullet/{i}.png') for i in range(1, 31)]

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Bullet.bullet_images[0]
        self.image = pygame.transform.scale(self.image, (320, 320))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.velx = 10
        self.animCount = 0

    def update(self, collide_group):
        self.rect.x += self.velx
        if self.animCount + 1 >= 60:
            self.animCount = 0
        self.image = Bullet.bullet_images[self.animCount // 2]
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.animCount += 1
        elem = [el for el in collide_group][0]
        if pygame.sprite.collide_mask(self, elem):
            self.kill()
            return 'killed'
        else:
            return 'alive'
