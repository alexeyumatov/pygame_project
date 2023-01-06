import pygame
from functions import load_image, flip
from groups import all_sprites, bullets, walls_group, tiles_group
from objects import Bullet

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

        self.rect.x, self.rect.y = 150, 260
        self.velx, self.vely = 0, 0
        self.width, self.height = self.image.get_width(), self.image.get_height()

        self.isColided_left, self.isColided_right = False, False
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
        if key[pygame.K_SPACE] and self.inJump is False:
            vl_y = -30
            self.inJump = True
        if key[pygame.K_SPACE] is False:
            self.inJump = False
        if key[pygame.K_a]:
            vl_x -= 12
            self.animCount += 1
            self.view = 'left'
            self.state = True
        if key[pygame.K_d]:
            vl_x += 12
            self.animCount += 1
            self.view = 'right'
            self.isFlipped, self.state = False, True
        if not key[pygame.K_d] and not key[pygame.K_a] and not self.onLadder:
            self.state = False
            if self.animCount + 1 >= 42:
                self.animCount = 0

            self.image = Player.idle_images[self.animCount // 7]
            if self.view == 'left':
                self.image = flip(self.image)

            self.animCount += 1

        if self.onLadder:
            self.image = Player.idle_images[0]
            if self.view == 'left':
                self.image = flip(self.image)
            if key[pygame.K_w]:
                ladder_vl_y -= 10
            if key[pygame.K_s] and not self.ladder_collide:
                ladder_vl_y += 10

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
        if not self.onLadder:
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
            if tile.rect.colliderect(self.rect.x, self.rect.y + vl_y, self.width, self.height):
                if self.vely < 0:
                    vl_y = tile.rect.bottom - self.rect.top
                    self.vely = 0
                elif self.vely >= 0:
                    vl_y = tile.rect.top - self.rect.bottom
                    self.vely = 0

        self.rect.x += vl_x
        if vl_y < -50:
            vl_y = 10
        self.rect.y += vl_y

    def shoot(self):
        if len(self.bulletList) > 3:
            return None
        ratio = 0
        if self.view == "left":
            ratio = 0.8
        else:
            ratio = 1.1
        bullet = Bullet(self.rect.centerx * ratio, self.rect.top * 1.2, self.view, walls_group, all_sprites, bullets)
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

    def collider(self, collide_group):
        if pygame.sprite.spritecollideany(self, collide_group):
            self.rect.x += 15
            if pygame.sprite.spritecollideany(self, collide_group):
                self.isColided_right = True
            else:
                self.isColided_left = True
            self.rect.x -= 15
        else:
            self.isColided_left, self.isColided_right = False, False

    def ladder_climb(self, collide_group, floor_group):
        hits = pygame.sprite.spritecollide(self, collide_group, False)
        if not hits:
            self.onLadder = False
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
