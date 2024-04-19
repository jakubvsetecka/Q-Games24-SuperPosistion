import copy
from modules.enemy import Enemy
from modules.player import Player
from modules.state import State, SuperpositionState
import pygame
import time

ADDENEMY = pygame.USEREVENT + 1
NOT = pygame.USEREVENT + 2
HADAMARD = pygame.USEREVENT + 3
PLAYER_ENEMY_COLLISION = pygame.USEREVENT + 4

class Event:
    def __init__(self, event_type):
        self.event_type = event_type

    def handle(self):
        pass

class AddEnemyEvent(Event):
    def __init__(self, enemies, state, screen_width, screen_height):
        super().__init__("ADDENEMY")
        self.enemies = enemies
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = state

    def handle(self):
        new_enemy = Enemy(self.screen_width, self.screen_height, state= self.state)
        self.enemies.add(new_enemy)

class NotEvent(Event):
    def __init__(self, player, in_superposition):
        super().__init__("NOT")
        self.player = player
        self.in_superposition = in_superposition

    def handle(self):
        if not self.in_superposition:
            self.player.flip()

class HadamardEvent(Event):
    def __init__(self, players, enemies, state):
        super().__init__("HADAMARD")
        self.players = players
        self.enemies = enemies
        self.state = state

    def handle(self):
        if self.state.superposition_state == SuperpositionState.SUPERPOSITION:
            self.state.superposition_state = SuperpositionState.NO_SUPERPOSITION
        else:
            self.state.superposition_state = SuperpositionState.SUPERPOSITION

        if self.state.superposition_state == SuperpositionState.NO_SUPERPOSITION:
            for enemy in self.enemies:
                enemy.exit_superposition()

            for player in self.players:
                player.exit_superposition()
        else:                                   # Going into superposition
            new_player = self.players.sprites()[0]
            new_player = copy.copy(self.players.sprites()[0])
            new_player.flip()
            self.players.add(new_player)

            for player in self.players:
                player.enter_superposition()

            for enemy in self.enemies:
                enemy.enter_superposition()


class PlayerEnemyCollisionEvent(Event):
    def __init__(self, player, enemies, state):
        super().__init__("PLAYER_ENEMY_COLLISION")
        self.player = player
        self.enemies = enemies
        self.state = state

    def handle(self):
        self.state.lives -= 1
        if self.state.lives == 0:
            self.state.game_over = True
        else:
            for enemy in self.enemies:
                enemy.kill()
            time.sleep(1)


class EventHandler:
    def __init__(self, enemies, players, state, screen):
        self.event_list = []
        self.state = state
        self.enemies = enemies
        self.players = players
        self.screen = screen
        self.top = screen.top
        self.bot = screen.bot
        self.left = screen.left
        self.right = screen.right

    def add_event(self, event):
        self.event_list.append(event)

    def set_timer(self, event_type, time_interval):
        pygame.time.set_timer(event_type, time_interval)

    def remove_event(self, event):
        self.event_list.remove(event)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == ADDENEMY:
                event = AddEnemyEvent(self.enemies, self.state, screen_height= self.bot, screen_width= self.right)
            elif e.type == NOT:
                try:
                    assert len(self.players) == 1
                except AssertionError:
                    print("Only one player can be in superposition")
                    continue
                print("NOT")
                self.screen.add_message("NOT", 0, self.screen.half_height)
                in_superposition = self.state.superposition_state == SuperpositionState.SUPERPOSITION
                event = NotEvent(self.players.sprites()[0], in_superposition)
            elif e.type == HADAMARD:
                print("HADAMARD")
                event = HadamardEvent(self.players, self.enemies, self.state)
            elif e.type == PLAYER_ENEMY_COLLISION:
                print("PLAYER_ENEMY_COLLISION")
                event = PlayerEnemyCollisionEvent(self.players, self.enemies, self.state)
            else:
                continue

            event.handle()