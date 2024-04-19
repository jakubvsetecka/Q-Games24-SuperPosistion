from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    K_w,
    K_s
)
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, tB, bB, lB, rB, color = (255, 255, 255), speed = 5, original = True):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

        self.rect.x = initial_x
        self.rect.y = initial_y

        self.topBoundary = tB
        self.bottomBoundary = bB
        self.leftBoundary = lB
        self.rightBoundary = rB

        self.speed = speed
        self.original_speed = speed

        self.in_superposition = False
        self.original = original

    def update(self, pressed_keys): # we move the rectangular with (x,y)
        speed = self.speed

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(speed, 0)
        # Keep player on the screen
        if self.rect.left < self.leftBoundary:
            self.rect.left = self.leftBoundary
        if self.rect.right > self.rightBoundary:
            self.rect.right = self.rightBoundary
        if self.rect.top <= self.topBoundary:
            self.rect.top = self.topBoundary
        if self.rect.bottom >= self.bottomBoundary:
            self.rect.bottom = self.bottomBoundary

    def destroy(self):
        self.kill()

    def enter_superposition(self):
        self.speed = 0

    def exit_superposition(self):
        self.speed = self.original_speed

    def flip(self):
        if not self.in_superposition:
            if self.topBoundary == 0:
                self.rect.y = self.rect.y + self.bottomBoundary
                self.topBoundary = self.bottomBoundary
                self.bottomBoundary = self.bottomBoundary * 2
            else:
                self.rect.y = self.rect.y - self.topBoundary
                self.topBoundary = 0
                self.bottomBoundary = self.bottomBoundary // 2
