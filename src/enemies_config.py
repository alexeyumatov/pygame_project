import pygame
from functions import load_image, flip
from groups import player_group, enemy_bullets, all_sprites
from objects import EnemyBullet


class RegularEnemy(pygame.sprite.Sprite):
    images = [load_image(f'enemies/regular_enemy/{i}.png') for i in range(1, 9)]

    def __init__(self, x, y, *groups):
        super(RegularEnemy, self).__init__(*groups)
        self.image = RegularEnemy.images[0]
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.animCount = 0
        self.counter = 0

        self.health_points = 85
        self.damage = 50

        self.view = 'right'
        self.velx = 0
        self.distance = 0

    def update(self):
        vl_x = 0

        # ANIMATION
        if self.animCount > 49:
            self.animCount = 0

        self.image = RegularEnemy.images[self.animCount // 7]
        if self.view == 'left':
            self.image = flip(self.image)
        self.animCount += 1

        # MOVEMENT
        if self.view == 'right':
            self.velx += 0.5
            if self.velx >= 20:
                self.velx = 20
            vl_x += self.velx
        elif self.view == 'left':
            self.velx -= 0.5
            if self.velx <= -20:
                self.velx = -20
            vl_x += self.velx

        self.distance += vl_x
        if abs(self.distance) >= 650:
            if self.view == 'right':
                self.view = 'left'
            else:
                self.view = 'right'
            self.distance = 0

        self.rect.x += vl_x

        # PLAYER COLLIDE
        player_collide = pygame.sprite.spritecollideany(self, player_group)
        if player_collide:
            if self.counter % 60 == 0:
                player_collide.damage(self.damage)
                self.counter = 0
            self.counter += 1
        else:
            self.counter = 0

    def incoming_damage(self, damage_amount):
        self.health_points -= damage_amount
        if self.health_points <= 0:
            self.kill()


class MiddleEnemy(pygame.sprite.Sprite):
    images = [load_image(f'enemies/middle_enemy/Enemy_2_Idle_{i}.png') for i in range(2, 10)]

    def __init__(self, x, y, *groups):
        super(MiddleEnemy, self).__init__(*groups)
        self.image = MiddleEnemy.images[0]
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.animCount = 0
        self.counter = 0

        self.velx = 0
        self.distance = 0
        self.isShoot = False

        self.view = 'right'
        self.isCollided = False

        self.health_points = 200
        self.damage = 100

    def update(self):
        vl_x = 0

        if self.animCount > 49:
            self.animCount = 0

        self.image = MiddleEnemy.images[self.animCount // 7]
        if self.view == 'right':
            self.image = flip(self.image)

        self.animCount += 1

        if self.view == 'right':
            self.velx += 0.5
            if self.velx >= 15:
                self.velx = 15
            vl_x += self.velx
        elif self.view == 'left':
            self.velx -= 0.5
            if self.velx <= -15:
                self.velx = -15
            vl_x += self.velx

        self.distance += vl_x
        if abs(self.distance) >= 500:
            if self.view == 'right':
                self.view = 'left'
            else:
                self.view = 'right'
            self.isShoot = False
            self.distance = 0

        if abs(self.distance) >= 250:
            self.isShoot = False

        elif abs(self.distance) == 250:
            self.isShoot = True

        if abs(self.distance) >= 100 and self.isShoot is False:
            if not self.isCollided:
                self.isShoot = True
                self.shoot()

        self.rect.x += vl_x

        player_collide = pygame.sprite.spritecollideany(self, player_group)
        if player_collide:
            self.isCollided = True
            if self.counter % 60 == 0:
                player_collide.damage(self.damage)
                self.counter = 0
            self.counter += 1
        else:
            self.isCollided = False
            self.counter = 0

    def incoming_damage(self, damage_amount):
        self.health_points -= damage_amount
        if self.health_points <= 0:
            self.kill()

    def shoot(self):
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        EnemyBullet(self.rect.x + ratio, self.rect.y + 145, self.view, all_sprites, enemy_bullets)
