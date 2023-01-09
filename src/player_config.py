import pygame
from functions import load_image, flip
from groups import all_sprites, bullets, walls_group, tiles_group, coins_group
from objects import Bullet
from src.db_functions import coins_update

g = 10


class Player(pygame.sprite.Sprite):
    idle_images = [load_image('hero/hero_static/Player_Static_Animation_1.png'),
                   load_image('hero/hero_static/Player_Static_Animation_2.png'),
                   load_image('hero/hero_static/Player_Static_Animation_3.png'),
                   load_image('hero/hero_static/Player_Static_Animation_4.png'),
                   load_image('hero/hero_static/Player_Static_Animation_5.png'),
                   load_image('hero/hero_static/Player_Static_Animation_6.png')]

    walk_images = [
        load_image('hero/hero_walk/Player_Walk_Animation_1.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_2.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_3.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_4.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_5.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_6.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_7.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_8.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_9.png'),
        load_image('hero/hero_walk/Player_Walk_Animation_10.png')]

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.idle_images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x, self.rect.y = 150, 1080
        self.velx, self.vely, self.ladder_vely = 0, 0, 0
        self.width, self.height = self.image.get_width(), self.image.get_height()

        self.animCount = 0
        self.view, self.isFlipped = "right", False
        self.state = False
        self.OnGround, self.onLadder = False, False
        self.inJump = False

        self.bullet_onScreen = False
        self.bulletList = []

    # collide_group
    def update(self):
        vl_x, vl_y = 0, 0
        ladder_vl_y = 0  # дополнительные переменные скорости

        # движение игрока
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.inJump and not self.onLadder and self.OnGround:
            vl_y = -2
            self.inJump = True
            self.OnGround = False

        if key[pygame.K_a]:
            if self.velx > 0:
                self.velx = 0
            self.velx -= 0.5
            if self.velx <= -14:
                self.velx = -14
            vl_x += self.velx
            self.animCount += 1
            self.view = 'left'
            self.state = True

        if key[pygame.K_d]:
            if self.velx < 0:
                self.velx = 0
            self.velx += 0.5
            if self.velx >= 14:
                self.velx = 14
            vl_x += self.velx
            self.animCount += 1
            self.view = 'right'
            self.isFlipped, self.state = False, True

        if not key[pygame.K_d] and not key[pygame.K_a]:
            self.state = False
            if self.velx > 0:
                self.velx -= 2
                if self.velx <= 0:
                    self.velx = 0
            elif self.velx < 0:
                self.velx += 2
                if self.velx >= 0:
                    self.velx = 0
            vl_x += self.velx

            # idle анимация
            if not self.onLadder:
                if self.animCount + 1 >= 42:
                    self.animCount = 0

                self.image = Player.idle_images[self.animCount // 7]
                if self.view == 'left':
                    self.image = flip(self.image)

                self.animCount += 1

        # лестница
        if self.onLadder:
            self.image = Player.idle_images[0]
            if self.view == 'left':
                self.image = flip(self.image)

            if key[pygame.K_w]:
                self.ladder_vely -= 0.5
                if self.ladder_vely <= -10:
                    self.ladder_vely = -10
                ladder_vl_y += self.ladder_vely

            if key[pygame.K_s] and not self.ladder_collide:
                self.ladder_vely += 0.5
                if self.ladder_vely >= 10:
                    self.ladder_vely = 10
                ladder_vl_y += self.ladder_vely
            if not key[pygame.K_s] and not key[pygame.K_w]:
                if self.ladder_vely > 0:
                    self.ladder_vely -= 2
                    if self.ladder_vely <= 0:
                        self.ladder_vely = 0
                    ladder_vl_y += self.ladder_vely
                if self.ladder_vely < 0:
                    self.ladder_vely += 2
                    if self.ladder_vely >= 0:
                        self.ladder_vely = 0
                    ladder_vl_y += self.ladder_vely

        if self.view == "left" and not self.isFlipped:
            self.image = flip(self.image)
            self.isFlipped = True

        if self.state and not self.onLadder:
            if self.animCount + 1 >= 60:
                self.animCount = 0

            self.image = Player.walk_images[self.animCount // 6]

            if self.view == "left":
                self.image = flip(self.image)

            self.animCount += 1

        # гравитация
        if not self.onLadder and not self.inJump:
            self.vely += 1
            if self.vely > 10:
                self.vely = 10
            vl_y += self.vely
        else:
            self.rect.y += ladder_vl_y

        # проверка коллайдов
        for tile in tiles_group:
            if tile.rect.colliderect(self.rect.x + vl_x, self.rect.y, self.width, self.height):
                vl_x = 0
                self.velx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + vl_y, self.width, self.height):
                if self.vely < 0:
                    vl_y = tile.rect.bottom - self.rect.top
                    self.vely = 0
                elif self.vely >= 0:
                    vl_y = tile.rect.top - self.rect.bottom
                    self.OnGround = True
                    self.vely = 0
                    self.inJump = False

        if pygame.sprite.spritecollide(self, coins_group, True):
            coins_update(1)

        if self.inJump:
            self.vely -= 2
            if self.vely <= -10:
                self.vely = -10
                self.inJump = False
            vl_y += self.vely

        self.rect.x += vl_x
        if vl_y < -150:
            vl_y = 10
        self.rect.y += vl_y

    def shoot(self):
        if len(self.bulletList) > 3:
            return None
        if self.view == "left":
            ratio = -30
        else:
            ratio = 150
        bullet = Bullet(self.rect.x + ratio, self.rect.y + 145, self.view, walls_group, all_sprites, bullets)
        self.bulletList.append(bullet)
        self.bullet_onScreen = True

    def bullet_update(self):
        if self.bullet_onScreen:
            for el in self.bulletList:
                state = el.update()
                if state == 'killed':
                    self.bulletList.remove(el)
            if len(bullets) == 0:
                self.bullet_onScreen = False

    def ladder_climb(self, collide_group, floor_group):
        hits = pygame.sprite.spritecollide(self, collide_group, False)
        if not hits:
            self.onLadder = False
            self.OnGround = False
            return False
        else:
            for el in collide_group:
                hits_mask = pygame.sprite.collide_mask(self, el)
                if hits_mask:
                    self.onLadder = True
                    if pygame.sprite.spritecollide(self, floor_group, False):
                        self.ladder_collide = True
                    else:
                        self.ladder_collide = False
                    return True
                else:
                    self.onLadder = False
