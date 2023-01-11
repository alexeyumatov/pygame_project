import pygame
from functions import load_image, flip
from groups import walls_group, enemies_group
from db_functions import bullets_damage_select


class Bullet(pygame.sprite.Sprite):
    images = [load_image(f'objects/bullet/{i}.png') for i in range(1, 7)]

    def __init__(self, x, y, player_view, *groups):
        super().__init__(*groups)
        self.image = Bullet.images[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect.x, self.rect.y = x, y
        if player_view == "left":
            self.velx = -20
        elif player_view == "right":
            self.velx = 20
        self.view = player_view
        self.animCount = 0

        self.damage = bullets_damage_select(1)

    def update(self):
        if self.animCount + 1 >= 42:
            self.animCount = 0
        self.image = Bullet.images[self.animCount // 7]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.view == "left":
            self.image = flip(self.image)
        self.animCount += 1

        self.rect.x += self.velx

        collided = pygame.sprite.spritecollideany(self, enemies_group)
        if collided:
            collided.incoming_damage(self.damage)
            self.kill()
            return 'killed'

        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
            return 'killed'
        else:
            return 'alive'


class Coin(pygame.sprite.Sprite):
    image = load_image("objects/coin/coin.png", -1)

    def __init__(self, pos_x, pos_y, *groups):
        super(Coin, self).__init__(*groups)
        self.image = Coin.image
        width, height = 50, 75
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect().move(pos_x * 128, 128 * pos_y)
