import pygame
import random
from src.functions import load_image, flip
from src.groups import walls_group, enemies_group, player_group, enemy_bullets, floor_group, thorn_group, all_sprites
from src.db_functions import bullets_damage_select, bullet_is_collidable_select, \
    stamina_select, stamina_update


class Bullet(pygame.sprite.Sprite):
    images = [load_image(f'hero/bullet/{i}.png') for i in range(1, 7)]

    def __init__(self, x, y, player_view, *groups):
        super().__init__(*groups)
        self.image = Bullet.images[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        if player_view == "left":
            self.velx = -20
        elif player_view == "right":
            self.velx = 20
        self.view = player_view
        self.animCount = 0

        self.damage = bullets_damage_select(1)

    def update(self):
        for el in player_group:
            hero = el
        if self.animCount + 1 >= 42:
            self.animCount = 0
        self.image = Bullet.images[self.animCount // 7]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.view == "left":
            self.image = flip(self.image)
        self.animCount += 1

        self.rect.x += self.velx

        if bullet_is_collidable_select(1):
            if pygame.sprite.spritecollide(self, enemy_bullets, True):
                self.kill()
                return 'killed'

        collided = pygame.sprite.spritecollideany(self, enemies_group)
        if collided and not collided.death_anim:
            collided.incoming_damage(self.damage)
            if hero.stamina < 100:
                stamina_update(1, 10)
            hero.stamina = stamina_select(1)
            self.kill()
            return 'killed'

        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
            return 'killed'
        else:
            return 'alive'


class UltimateAttack(pygame.sprite.Sprite):
    images = [load_image(f'hero/ultimate_attack/eye_fire_blue{i}.png', -1) for i in range(1, 8)]

    def __init__(self, x, y, player_view, *groups):
        super(UltimateAttack, self).__init__(*groups)
        self.image = UltimateAttack.images[0]
        self.image = pygame.transform.scale(self.image, (96, 72))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.view = player_view
        if self.view == 'left':
            self.velx = -28
        elif self.view == 'right':
            self.velx = 28
            self.image = flip(self.image)

        self.animCount = 0

        self.damage = 70
        self.collide_count = 0

    def update(self):
        if self.animCount >= 49:
            self.animCount = 0
        self.image = UltimateAttack.images[self.animCount // 7]
        if self.view == 'right':
            self.image = flip(self.image)
        self.image = pygame.transform.scale(self.image, (96, 72))
        self.animCount += 1

        self.rect.x += self.velx

        collided = pygame.sprite.spritecollideany(self, enemies_group)
        if collided:
            self.collide_count += 1
            if self.collide_count == 1:
                if self.velx > 10:
                    self.velx -= 2
                elif self.velx < -10:
                    self.velx += 10
            collided.incoming_damage(self.damage)
        else:
            self.collide_count = 0

        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
            return 'killed'
        else:
            return 'alive'


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_view, *groups):
        super(EnemyBullet, self).__init__(*groups)
        self.images = [load_image(f"enemies/middle_enemy/bullets/enemy_bullet_{i}.png") for i in range(1, 7)]
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        if enemy_view == 'left':
            self.velx = -23
        elif enemy_view == 'right':
            self.velx = 23
        self.rect.x, self.rect.y = x, y

        self.view = enemy_view
        self.animCount = 0

        self.damage = 30

    def update(self):
        if self.animCount + 1 >= 42:
            self.animCount = 0
        self.image = self.images[self.animCount // 7]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.view == "left":
            self.image = flip(self.image)
        self.animCount += 1

        self.rect.x += self.velx

        collided = pygame.sprite.spritecollideany(self, player_group)
        if collided:
            collided.damage(self.damage)
            self.poison()
            self.kill()

        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
            return 'killed'
        else:
            return 'alive'

    def poison(self):
        pass


class PoisonBullet(EnemyBullet):
    def __init__(self, x, y, player_view, *groups):
        super(PoisonBullet, self).__init__(x, y, player_view, *groups)
        self.images = [load_image(f'enemies/'
                                  f'hard_enemy/bullets/'
                                  f'enemy_3_bullet_{i}.png')
                       for i in range(1, 7)]
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.view = player_view
        if self.view == 'right':
            self.velx = 30
        elif self.view == 'left':
            self.velx = -30

    def poison(self):
        for el in player_group:
            el.isPoisoned = True


class Coin(pygame.sprite.Sprite):
    image = load_image("objects/coin/coin.png", -1)

    def __init__(self, pos_x, pos_y, *groups):
        super(Coin, self).__init__(*groups)
        self.image = Coin.image
        width, height = 50, 75
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect().move(pos_x * 128, 128 * pos_y)


class Fountain(pygame.sprite.Sprite):
    images = [load_image(f"objects/fountain/{i}.png") for i in range(1, 8)]

    def __init__(self, pos_x, pos_y, *groups):
        super(Fountain, self).__init__(*groups)
        self.image = Fountain.images[0]
        self.rect = self.image.get_rect().move(
            pos_x * 128, pos_y * 128 - 47)
        self.animCount = 0
        self.isPressed = False
        self.heal_cooldown = 1

    def update(self):
        if self.animCount >= 49:
            self.animCount = 0

        self.image = Fountain.images[self.animCount // 7]

        self.animCount += 1

        if self.isPressed:
            if self.heal_cooldown // 120 == 1:
                for el in player_group:
                    el.isPoisoned = False
                self.heal_cooldown = 0
            self.heal_cooldown += 1
        else:
            self.heal_cooldown = 0


class Thorn(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Thorn, self).__init__(*groups)
        self.damage = 40
        self.counter = 0
        self.animCount = 0
        self.is_poisonous = False

    def update(self):
        player_collide = pygame.sprite.spritecollideany(self, player_group)
        if player_collide:
            if pygame.sprite.collide_mask(player_collide, self):
                if self.counter % 60 == 0:
                    player_collide.damage(self.damage)
                    if self.is_poisonous:
                        player_collide.isPoisoned = True
                    self.counter = 1
                else:
                    self.counter += 1
        else:
            self.counter = 0


class StaticThorn(Thorn):
    image = load_image("objects/thorns/static/thorn.png")

    def __init__(self, pos_x, pos_y, *groups):
        super(StaticThorn, self).__init__(*groups)
        self.image = StaticThorn.image
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x * 128 + 48, pos_y * 128 + 80
        )


class PoisonousThorn(Thorn):
    image = load_image("objects/thorns/poisonous/poisonous_thorn.png")

    def __init__(self, pos_x, pos_y, *groups):
        super(PoisonousThorn, self).__init__(*groups)
        self.image = PoisonousThorn.image
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x * 128 + 48, pos_y * 128 + 80
        )
        self.is_poisonous = True


class MovingThorn(Thorn):
    image = [load_image(f"objects/thorns/moving/thorn_{i}.png") for i in range(1, 26)]

    def __init__(self, pos_x, pos_y, *groups):
        super(MovingThorn, self).__init__(*groups)
        self.image = MovingThorn.image[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x * 128, pos_y * 128 + 64
        )
        self.velx = 0
        self.view = 'right'
        self.distance = 0

    def update(self):
        vl_x = 0

        if self.animCount >= 50:
            self.animCount = 0

        self.image = MovingThorn.image[self.animCount // 2]
        self.image = pygame.transform.scale(self.image, (64, 64))

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
            if self.view == 'right':
                self.view = 'left'
            else:
                self.view = 'right'
            self.distance = 0
            vl_x = 0

        self.rect.x += vl_x

        player_collide = pygame.sprite.spritecollideany(self, player_group)
        if player_collide:
            if pygame.sprite.collide_mask(player_collide, self):
                if self.counter % 60 == 0:
                    player_collide.damage(self.damage)
                    if self.is_poisonous:
                        player_collide.isPoisoned = True
                    self.counter = 1
                else:
                    self.counter += 1
        else:
            self.counter = 0


class FallingThorn(Thorn):
    image = load_image("objects/thorns/falling/falling_thorn.png")

    def __init__(self, pos_x, pos_y, *groups):
        super(FallingThorn, self).__init__(*groups)
        self.image = FallingThorn.image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y
        )
        self.vel_y = 60

    def update(self):
        player_collide = pygame.sprite.spritecollideany(self, player_group)
        if player_collide:
            if pygame.sprite.collide_mask(self, player_collide):
                if self.counter % 60 == 0:
                    player_collide.damage(self.damage)
                    self.counter = 1
                else:
                    self.counter += 1
        else:
            self.counter = 0
        for tile in floor_group:
            if tile.rect.colliderect(self.rect.x, self.rect.y, 64, 64):
                self.kill()
        self.rect.y += self.vel_y


class HostileBlock(pygame.sprite.Sprite):
    image = load_image('Locations/hostile_block.png')

    def __init__(self, pos_x, pos_y, *groups):
        super(HostileBlock, self).__init__(*groups)
        self.image = HostileBlock.image
        self.rect = self.image.get_rect().move(
            pos_x * 128, pos_y * 128
        )
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        coords = [[random.randint(130, 3540), 160] for _ in range(10)]
        collide = pygame.sprite.spritecollideany(self, player_group)
        if collide:
            if pygame.sprite.collide_mask(self, collide):
                for i in range(10):
                    pos_x, pos_y = coords[i][0], coords[i][1]
                    FallingThorn(pos_x, pos_y, all_sprites, thorn_group)
                self.kill()
