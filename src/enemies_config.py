import pygame
from functions import load_image, flip
from groups import player_group, enemy_bullets, all_sprites
from objects import EnemyBullet, PoisonBullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Enemy, self).__init__(*groups)

        self.animCount = 0
        self.death_animCount = 0
        self.death_time = 0
        self.view = 'right'
        self.velx = 0
        self.distance = 0

        self.view = 'right'
        self.isCollided = False
        self.death_anim = False

        self.images = []
        self.death_images = []

        self.damage = 0
        self.health_points = 0

    def update(self):
        vl_x = 0

        if self.death_anim:
            if self.death_time < 60:
                self.death_time += 1
                self.death()
            elif self.death_time >= 60:
                self.kill()
        else:

            if self.animCount > 49:
                self.animCount = 0

            self.image = self.images[self.animCount // 7]
            if self.view == 'right':
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
                if not self.isCollided:
                    self.shoot()
                if self.view == 'right':
                    self.view = 'left'
                else:
                    self.view = 'right'
                self.distance = 0

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

    def shoot(self):
        pass

    def incoming_damage(self, damage_amount):
        self.health_points -= damage_amount
        if self.health_points <= 0:
            self.death_anim = True

    def death(self):
        if self.death_animCount >= 60:
            self.death_animCount = 0

        self.image = self.death_images[self.death_animCount // 5]

        self.death_animCount += 1


class RegularEnemy(Enemy):

    def __init__(self, x, y, *groups):
        super(RegularEnemy, self).__init__(*groups)
        self.images = [load_image(f'enemies/regular_enemy/{i}.png') for i in range(1, 9)]
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.death_images = \
            [load_image(f'enemies/regular_enemy/enemy_death/{i}.png') for i in range(1, 13)]
        self.animCount = 0
        self.counter = 0

        self.health_points = 45
        self.damage = 30

        self.view = 'right'
        self.velx = 0
        self.distance = 0


class MiddleEnemy(Enemy):
    def __init__(self, x, y, *groups):
        super(MiddleEnemy, self).__init__(*groups)
        self.images = [load_image(f'enemies/middle_enemy/Enemy_2_Idle_{i}.png')
                       for i in range(2, 10)]
        self.death_images = [load_image(f'enemies/middle_enemy/enemy_death/{i}.png')
                             for i in range(1, 13)]
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.animCount = 0
        self.counter = 0

        self.velx = 0
        self.distance = 0

        self.view = 'right'
        self.isCollided = False

        self.health_points = 150
        self.damage = 50

    def shoot(self):
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        EnemyBullet(self.rect.x + ratio, self.rect.y + 145, self.view, all_sprites, enemy_bullets)


class HardEnemy(Enemy):
    def __init__(self, x, y, *groups):
        super(HardEnemy, self).__init__(*groups)
        self.images = [load_image(f'enemies/hard_enemy/enemy_3_idle_{i}.png')
                       for i in range(1, 13)]
        self.death_images = [load_image(f'enemies/hard_enemy/enemy_death/{i}.png')
                             for i in range(1, 13)]
        self.image = self.images[0]
        self.animCount = 0
        self.rect = self.image.get_rect().move(
            x * 128, y * 128)

        self.view = 'right'

        self.health_points = 200
        self.damage = 70

        self.velx = 0
        self.distance = 0
        self.isCollided = False

    def shoot(self):
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        PoisonBullet(self.rect.x + ratio, self.rect.y + 130, self.view, all_sprites, enemy_bullets)
