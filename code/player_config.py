import pygame
from load_image import load_image
from groups import all_sprites

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
        self.rect.x = 100
        self.rect.y = 150
        self.velx = 0
        self.vely = 0
        self.isColided_left, self.isColided_right = False, False
        self.phase, self.animCount = 0, 0
        self.view = "right"
        self.state = True
        self.OnGround = False

    # collide_group
    def update(self, collide_group):
        elem = [el for el in collide_group][0]

        if not pygame.sprite.collide_mask(self, elem) and self.phase == 0:
            self.OnGround = False

        if self.OnGround is False and self.phase == 0:
            self.fall(collide_group)

        # СТОИМ НА МЕСТЕ И ОТДЫХАЕМ
        if self.phase == 0 and self.state and self.OnGround is True:
            self.vely = 0

            if self.animCount + 1 >= 42:
                self.animCount = 0

            self.image = Player.idle_images[self.animCount // 7]

            if self.view == "left":
                self.flip()

            self.animCount += 1

        # ХОДИМ
        if not self.state:
            if self.phase > 0:
                pass
            else:
                self.rect.y -= 15

            if self.animCount + 1 >= 60:
                self.animCount = 0

            self.image = Player.walk_images[self.animCount // 6]

            if self.view == "left":
                self.flip()

            self.animCount += 1

        # ПРЫГАЕМ (ПАДЕНИЕ)
        if self.phase > 0:
            self.OnGround = False
            self.phase -= 2
            self.vely += g / 30
            self.rect.y += 30 * self.vely / 20

    def acceleration(self, left, right):
        self.state = True
        if not self.isColided_left:
            if left:
                self.state = False
                self.OnGround = True
                if self.view != "left":
                    self.view = "left"
                    self.flip()
                if self.velx < 13:
                    self.velx += 0.6
                self.rect = self.rect.move(-self.velx, 0)

        if not self.isColided_right:
            if right:
                self.state = False
                self.OnGround = True
                if self.view != "right":
                    self.view = "right"
                    self.flip()
                if self.velx < 13:
                    self.velx += 0.6
                self.rect = self.rect.move(self.velx, 0)

    def stop(self, left, right):
        if not self.isColided_left:
            if left:
                self.OnGround = True
                if self.velx > 0:
                    self.velx -= 2
                else:
                    self.velx = 0
                self.rect = self.rect.move(-self.velx, 0)

        if not self.isColided_right:
            if right:
                self.OnGround = True
                if self.velx > 0:
                    self.velx -= 2
                else:
                    self.velx = 0
                self.rect = self.rect.move(self.velx, 0)

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

    def fall(self, collide_group):
        elem = [el for el in collide_group][0]
        while self.OnGround is False:
            if pygame.sprite.collide_mask(self, elem):
                self.OnGround = True
                return True
            if not pygame.sprite.collide_mask(self, elem):
                self.rect.y += 1
                self.OnGround = False

