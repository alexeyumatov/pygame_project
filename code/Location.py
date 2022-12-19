import pygame
from load_image import load_image
from groups import all_sprites


class Location(pygame.sprite.Sprite):
    image = load_image('Locations/Loc2.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Location.image
        self.rect = self.image.get_rect()
        self.rect.y = 1080 - int(self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)
        print(self.mask)


