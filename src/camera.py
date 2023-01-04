import pygame


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def apply(self, target):
        return target.rect.move(self.state.topleft)


def camera_func(camera, target_rect):
    l = -target_rect.x + 1920 / 2
    t = -target_rect.y + 1080 / 2
    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(camera.width - 1920), l)
    t = max(-(camera.height - 1080), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)
