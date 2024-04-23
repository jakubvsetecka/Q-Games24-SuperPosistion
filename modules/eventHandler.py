import copy
import random
from modules.enemy import Enemy
from modules.player import Player
from modules.state import State, SuperpositionState
import pygame
import time

ADDENEMY = pygame.USEREVENT + 1
NOT = pygame.USEREVENT + 2
HADAMARD = pygame.USEREVENT + 3
PLAYER_ENEMY_COLLISION = pygame.USEREVENT + 4
GAME_OVER = pygame.USEREVENT + 5
ADD_BULLET = pygame.USEREVENT + 6

class Event:
    def __init__(self, event_type):
        self.event_type = event_type

    def handle(self):
        pass

class AddBulletEvent(Event):
    def __init__(self, bullets, players, state, screen):
        super().__init__("ADDBULLET")
        self.bullets = bullets
        self.players = players
        self.state = state
        self.screen = screen

    def handle(self):
        for player in self.players:
            player.shoot(self.bullets)

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
                if player.original:
                    player.exit_superposition()
                else:
                    player.kill()
        else:                                   # Going into superposition
            if self.players.sprites():  # Ensure there is at least one player
                new_player = self.players.sprites()[0].clone()
                new_player.flip()
                self.players.add(new_player)

            for player in self.players:
                player.enter_superposition()

            for enemy in self.enemies:
                enemy.enter_superposition()


class PlayerEnemyCollisionEvent(Event):
    def __init__(self, players, enemies, state):
        super().__init__("PLAYER_ENEMY_COLLISION")
        self.players = players
        self.enemies = enemies
        self.state = state

    def handleSuperposition(self):
        assert len(self.players) == 2
        true_player = self.players.sprites()[random.randint(0, len(self.players) - 1)]
        true_player.original = True
        true_player.exit_superposition()

        for player in self.players:
            if player != true_player:
                player.kill()
                self.players.remove(player)

        self.state.superposition_state = SuperpositionState.NO_SUPERPOSITION

    def handle(self):
        if self.state.superposition_state == SuperpositionState.SUPERPOSITION:
            self.handleSuperposition()
        else:
            self.state.lives -= 1
            if self.state.lives == 0:
                self.state.game_over = True
            else:
                time.sleep(1)
                for enemy in self.enemies:
                    enemy.kill()

class GameOverEvent(Event):
    def __init__(self, state, screen):
        super().__init__("GAME_OVER")
        self.state = state
        self.screen = screen

    def handle(self):
        self.screen.fill()
        msg = "Game Over"
        score = f"Score: {self.state.score}"
        self.screen.print_message("Game Over", self.screen.half_width - 4*len(msg), self.screen.half_height)
        self.screen.print_message(score, self.screen.half_width - 3*len(score), self.screen.half_height + 40)
        pygame.display.flip()
        time.sleep(5)
        self.state.keep_running = False


class EventHandler:
    def __init__(self, enemies, players, bullets, state, screen):
        self.event_list = []
        self.state = state
        self.enemies = enemies
        self.players = players
        self.bullets = bullets
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
                self.screen.add_message("HADAMARD", 0, self.screen.half_height)
                event = HadamardEvent(self.players, self.enemies, self.state)
            elif e.type == PLAYER_ENEMY_COLLISION:
                print("PLAYER_ENEMY_COLLISION")
                event = PlayerEnemyCollisionEvent(self.players, self.enemies, self.state)
            elif e.type == GAME_OVER:
                print("GAME_OVER")
                event = GameOverEvent(self.state, self.screen)
            elif e.type == ADD_BULLET:
                print("ADD_BULLET")
                event = AddBulletEvent(self.bullets, self.players, self.state, self.screen)
            else:
                continue

            event.handle()