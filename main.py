import pygame
from pygame.locals import (
    K_ESCAPE
)
import random
import time

from modules.player import Player
from modules.enemy import Enemy
from modules.screenHandler import ScreenHandler
from modules.eventHandler import EventHandler, ADDENEMY, NOT, HADAMARD, PLAYER_ENEMY_COLLISION
from modules.state import State

#===================================================================================================

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
HALF_HEIGHT = SCREEN_HEIGHT // 2
INITIAL_PLAYER_SPEED = 10

PLAYER_COLOR = (255, 255, 255) # white color
BACKGROUND_COLOR=(255, 182, 193) # pink color

CREATING_ENEMY_TIME_INTERVAL = 250 # later we can set it to different values if we wish
NOT_TIME_INTERVAL = random.randint(500, 1000) * 100000
HADAMARD_TIME_INTERVAL = random.randint(500, 1000) * 3

#===================================================================================================

def main():
    pygame.init()
    state = State()
    screen = ScreenHandler(SCREEN_WIDTH, SCREEN_HEIGHT, (BACKGROUND_COLOR), state)

    # Set players
    players = pygame.sprite.Group()
    player = Player(0, 0, screen.top, screen.half_height, screen.left, screen.right, state, PLAYER_COLOR, INITIAL_PLAYER_SPEED)
    players.add(player)

    # Set enemies
    enemies = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(players, enemies, screen)

    # Add events
    eventHandler = EventHandler(enemies= enemies, players= players, state= state, screen= screen)
    eventHandler.add_event(ADDENEMY)
    eventHandler.add_event(NOT)
    eventHandler.add_event(HADAMARD)
    eventHandler.add_event(PLAYER_ENEMY_COLLISION)
    eventHandler.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)
    eventHandler.set_timer(NOT, NOT_TIME_INTERVAL)
    eventHandler.set_timer(HADAMARD, HADAMARD_TIME_INTERVAL)


    running = True
    while running:

        eventHandler.handle_events()
        all_sprites.add(*enemies, players)

        screen.fill()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]: running = False

        all_sprites.update(pressed_keys)

        # Collision detection
        for player in players:
            if pygame.sprite.spritecollideany(player, enemies):
                pygame.event.post(pygame.event.Event(PLAYER_ENEMY_COLLISION))

        for entity in all_sprites:
            if entity != screen:
                screen.blit(entity)

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()