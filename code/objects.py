import pygame
from load_image import load_image


class Ladder(pygame.sprite.Sprite):
    image = load_image('objects/Ladder.png', -1)

    def __init__(self, *groups):
        super(Ladder, self).__init__(*groups)
        self.image = Ladder.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 500
        self.rect.y = 400
