from src.config import *
from src.functions import load_image, flip
from src.groups import player_group, enemy_bullets, all_sprites, tiles_group
from src.objects import EnemyBullet, PoisonBullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Enemy, self).__init__(*groups)

        self.animCount = 0
        self.death_animCount = 0
        self.death_time = 0

        self.width, self.height = 0, 0

        self.view = 'right'
        self.velx = 0
        self.vely = 0
        self.distance = 0
        self.OnGround = False

        self.type = 'tank'
        self.bullet_count = 1

        self.view = 'right'
        self.isCollided = False
        self.death_anim = False

        self.images = []
        self.death_images = []

        self.damage = 0
        self.health_points = 0

    def update(self):
        hero = [el for el in player_group][0]
        vl_x, vl_y = 0, 0

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

            self.vely += 1
            if self.vely > 10:
                self.vely = 10
            vl_y += self.vely

            if abs(hero.rect.y - self.rect.y) < 300 and abs(hero.rect.x - self.rect.x) < 2500:
                distance = 20 if self.type == 'tank' else 800
                if self.type == 'shooter':
                    if self.bullet_count % 70 == 0:
                        self.shoot()
                        self.bullet_count = 1
                    else:
                        self.bullet_count += 1
                if abs(hero.rect.x - self.rect.x) < distance:
                    vl_x = 0
                    self.view = 'right' if hero.rect.x >= self.rect.x else 'left'
                elif hero.rect.x > self.rect.x:
                    vl_x = 8
                    self.view = 'right'
                else:
                    vl_x = -8
                    self.view = 'left'
                self.distance = 0

            # COLLIDERS
            for tile in tiles_group:
                if tile.rect.colliderect(self.rect.x + vl_x, self.rect.y,
                                         self.width, self.height):
                    vl_x = 0
                    self.velx = 0
                    if self.view == 'right':
                        self.view = 'left'
                    else:
                        self.view = 'right'
                    self.distance = 0
                if tile.rect.colliderect(self.rect.x, self.rect.y + vl_y,
                                         self.width, self.height):
                    if self.vely < 0:
                        vl_y = tile.rect.bottom - self.rect.top
                        self.vely = 0
                    elif self.vely >= 0:
                        vl_y = tile.rect.top - self.rect.bottom
                        self.OnGround = True
                        self.vely = 0

            self.distance += vl_x
            if abs(self.distance) >= 500:
                if not self.isCollided:
                    self.shoot()
                if self.view == 'right':
                    self.view = 'left'
                else:
                    self.view = 'right'
                self.distance = 0
                vl_x = 0

            self.rect.x += vl_x
            if vl_y < -150:
                vl_y = 10
            self.rect.y += vl_y

            player_collide = pygame.sprite.spritecollideany(self, player_group)
            if player_collide:
                self.isCollided = True
                if self.counter % 60 == 0:
                    if not player_collide.dash:
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
        self.images = \
            [load_image(f'enemies/regular_enemy/{i}.png') for i in range(1, 9)]
        self.image = self.images[0]
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.death_images = \
            [load_image(f'enemies/regular_enemy/'
                        f'enemy_death/{i}.png') for i in range(1, 13)]
        self.animCount = 0
        self.counter = 0

        self.health_points = 45
        self.damage = 30

        self.type = 'tank'

        self.view = 'right'
        self.velx = 0
        self.distance = 0


class MiddleEnemy(Enemy):
    def __init__(self, x, y, *groups):
        super(MiddleEnemy, self).__init__(*groups)
        self.images = [load_image(f'enemies/middle_enemy/Enemy_2_Idle_{i}.png')
                       for i in range(2, 10)]
        self.death_images = [load_image(f'enemies/'
                                        f'middle_enemy/enemy_death/{i}.png')
                             for i in range(1, 13)]
        self.image = self.images[0]
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(
            128 * x, 128 * y)
        self.animCount = 0
        self.counter = 0

        self.velx = 0
        self.distance = 0

        self.view = 'right'
        self.isCollided = False

        self.type = 'shooter'

        self.health_points = 150
        self.damage = 50

    def shoot(self):
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        EnemyBullet(self.rect.x + ratio, self.rect.y + 145,
                    self.view, all_sprites, enemy_bullets)


class HardEnemy(Enemy):
    def __init__(self, x, y, *groups):
        super(HardEnemy, self).__init__(*groups)
        self.images = [load_image(f'enemies/hard_enemy/enemy_3_idle_{i}.png')
                       for i in range(1, 13)]
        self.death_images = [load_image(f'enemies/hard_enemy/'
                                        f'enemy_death/{i}.png')
                             for i in range(1, 13)]
        self.image = self.images[0]
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.animCount = 0
        self.rect = self.image.get_rect().move(
            x * 128, y * 128)

        self.view = 'right'

        self.health_points = 200
        self.damage = 70

        self.type = 'shooter'

        self.velx = 0
        self.distance = 0
        self.isCollided = False

    def shoot(self):
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        PoisonBullet(self.rect.x + ratio, self.rect.y + 130,
                     self.view, all_sprites, enemy_bullets)
