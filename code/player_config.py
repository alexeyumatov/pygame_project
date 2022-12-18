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

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.idle_images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 200
        self.rect.y = 150
        self.ground = 0
        self.velx = 0
        self.vely = 0
        self.phase, self.animCount = 0, 0
        self.view = "right"

    def update(self):
        if self.phase == 0:
            self.vely = 0
            self.rect.y = self.ground

            # if self.animCount + 1 >= 42:
            #     self.animCount = 0

            # self.image = Player.idle_images[self.animCount // 7]
            # self.animCount += 1

        elif self.phase > 0:
            self.phase -= 2
            self.vely += g / 30
            self.rect.y += 30 * self.vely / 20

    def acceleration(self, left, right):
        if left:
            if self.view != "left":
                self.view = "left"
                self.flip()
            if self.velx < 15:
                self.velx += 2
            self.rect = self.rect.move(-self.velx, 0)

        elif right:
            if self.view != "right":
                self.view = "right"
                self.flip()
            if self.velx < 15:
                self.velx += 2
            self.rect = self.rect.move(self.velx, 0)

    def stop(self, left, right):
        if left:
            if self.velx > 0:
                self.velx -= 2
            else:
                self.velx = 0
            self.rect = self.rect.move(-self.velx, 0)
        elif right:
            if self.velx > 0:
                self.velx -= 2
            else:
                self.velx = 0
            self.rect = self.rect.move(self.velx, 0)

    def player_init(self, collide_group):
        elem = [el for el in collide_group][0]
        if pygame.sprite.collide_mask(self, elem):
            self.ground += self.rect.y
            return True
        if not pygame.sprite.collide_mask(self, elem):
            self.rect.y += 2

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
