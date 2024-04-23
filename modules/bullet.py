import pygame
from modules.state import SuperpositionState

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, state, color, speed = 10, boundary = 800):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = state
        self.speed = 10
        self.boundary = boundary

    def update(self, _pressed_keys):
        if self.state == SuperpositionState.SUPERPOSITION:
            self.rect.move_ip(-self.speed, 0)
        else:
            self.rect.move_ip(self.speed, 0)
        if self.rect.left >= self.boundary:
            self.kill()