from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s
)
import pygame
import random
from modules.state import State, SuperpositionState

ENEMY_MAX_SPEED = 3
ENEMY_MIN_SPEED = 1
ENEMY_COLOR = (255, 255, 255)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, state, enemy_min_speed = ENEMY_MIN_SPEED, enemy_max_speed = ENEMY_MAX_SPEED, color= ENEMY_COLOR):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )

        self.min_speed = random.randint(2,4) * enemy_min_speed
        self.max_speed = random.randint(2,4) * enemy_max_speed

        self.state = state
        if state.superposition_state == SuperpositionState.SUPERPOSITION:
            self.speed = self.min_speed
        else:
            self.speed = self.max_speed

        self.screen_height = screen_height

    def update(self, pressed_keys):
        if not self.state.superposition_state == SuperpositionState.SUPERPOSITION:
            self.rect.move_ip(-self.speed, 0)
            pass
        else:
            self.rect.move_ip(-self.speed, 0)
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                self.rect.move_ip(0, -self.speed)
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                self.rect.move_ip(0, self.speed)
            # Keep player on the screen
            if self.rect.bottom <= 0:
                self.rect.y = self.screen_height - self.rect.height
            elif self.rect.top >= self.screen_height:
                self.rect.y = 0
        if self.rect.right < 0:
            self.kill()

    def enter_superposition(self):
        self.speed = self.min_speed

    def exit_superposition(self):
        self.speed = self.max_speed
