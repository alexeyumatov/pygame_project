import pygame
from load_image import load_image
from groups import all_sprites, bullets, right_walls
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

        self.rect.x, self.rect.y = 100, 150
        self.velx, self.vely = 0, 0

        self.isColided_left, self.isColided_right = False, False
        self.animCount = 0
        self.view = "right"
        self.state = True
        self.OnGround, self.onLadder = False, False

        self.bullet_onScreen = False
        self.bulletList = []

    # collide_group
    def update(self, collide_group):
        elem = [el for el in collide_group][0]
        hits = pygame.sprite.collide_mask(self, elem)

        if self.vely > 0:
            if hits:
                self.rect.y = elem.rect.top
                self.vely = 0

        if not hits:
            self.rect.y += g

        # СТОИМ НА МЕСТЕ И ОТДЫХАЕМ
        if self.state and self.OnGround is True:
            self.vely = 0

            if self.animCount + 1 >= 42:
                self.animCount = 0

            self.image = Player.idle_images[self.animCount // 7]

            if self.view == "left":
                self.flip()

            self.animCount += 1

        # ХОДИМ
        if not self.state:

            if self.animCount + 1 >= 60:
                self.animCount = 0

            self.image = Player.walk_images[self.animCount // 6]

            if self.view == "left":
                self.flip()

            self.animCount += 1

        if self.bullet_onScreen:
            for el in self.bulletList:
                state = el.update(right_walls)
                if state == 'killed':
                    self.bulletList.remove(el)
            if len(bullets) == 0:
                self.bullet_onScreen = False

    def acceleration(self, *parameters):
        self.state = True
        if not self.isColided_left:
            if parameters[0]:
                self.state = False
                self.OnGround = True
                if self.view != "left":
                    self.view = "left"
                    self.flip()
                if self.velx < 13:
                    self.velx += 0.6
                self.rect = self.rect.move(-self.velx, 0)

        if not self.isColided_right:
            if parameters[1]:
                self.state = False
                self.OnGround = True
                if self.view != "right":
                    self.view = "right"
                    self.flip()
                if self.velx < 13:
                    self.velx += 0.6
                self.rect = self.rect.move(self.velx, 0)

        if self.onLadder:
            if not self.ladder_collide:
                if parameters[3]:
                    if self.vely < 12:
                        self.vely += 0.6
                    self.rect = self.rect.move(0, self.vely)
            if parameters[2]:
                if self.vely < 12:
                    self.vely += 0.6
                self.rect = self.rect.move(0, -self.vely)

    def stop(self, *parameters):
        if not self.isColided_left:
            if parameters[0]:
                self.OnGround = True
                if self.velx > 0:
                    self.velx -= 2
                else:
                    self.velx = 0
                self.rect = self.rect.move(-self.velx, 0)

        if not self.isColided_right:
            if parameters[1]:
                self.OnGround = True
                if self.velx > 0:
                    self.velx -= 2
                else:
                    self.velx = 0
                self.rect = self.rect.move(self.velx, 0)

        if self.onLadder:
            if not self.ladder_collide:
                if parameters[3]:
                    if self.vely > 0:
                        self.vely -= 2
                    else:
                        self.vely = 0
                    self.rect = self.rect.move(0, self.vely)
            if parameters[2]:
                if self.vely > 0:
                    self.vely -= 2
                else:
                    self.vely = 0
                self.rect = self.rect.move(0, -self.vely)

    def shoot(self):
        if len(self.bulletList) > 3:
            return None
        bullet = Bullet(self.rect.centerx, self.rect.top * 1.5, all_sprites, bullets)
        self.bulletList.append(bullet)
        self.bullet_onScreen = True

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def collider(self, left_walls, right_walls):
        left_wall = [el for el in left_walls][0]
        right_wall = [el for el in right_walls][0]
        if pygame.sprite.collide_mask(self, left_wall):
            self.isColided_left = True
        else:
            self.isColided_left = False
        if pygame.sprite.collide_mask(self, right_wall):
            self.isColided_right = True
        else:
            self.isColided_right = False

    def ladder_climb(self, collide_group, floor_collide):
        ladders, floor = [el for el in collide_group][0], [el for el in floor_collide][0]

        hits = pygame.sprite.collide_mask(self, ladders)
        if not hits:
            self.onLadder = False
            return False
        else:
            self.onLadder = True
            if pygame.sprite.collide_mask(self, floor):
                self.ladder_collide = True
            else:
                self.ladder_collide = False
            return True
