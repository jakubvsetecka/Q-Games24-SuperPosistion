import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
)
import random
import time

#===================================================================================================

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
HALF_HEIGHT = SCREEN_HEIGHT // 2
INITIAL_PLAYER_SPEED = 10
PLAYER_COLOR = (255, 255, 255) # white color

BACKGROUND_COLOR=(255, 182, 193) # pink color

ENEMY_MAX_SPEED = 5
ENEMY_MIN_SPEED = 1

IN_SUPERPOSITION = False

ADDENEMY = pygame.USEREVENT + 1 # each event is associated with an integer
NOT = pygame.USEREVENT + 2
HADAMARD = pygame.USEREVENT + 3

CREATING_ENEMY_TIME_INTERVAL = 250 # later we can set it to different values if we wish
NOT_TIME_INTERVAL = random.randint(500, 1000) * 5
HADAMARD_TIME_INTERVAL = random.randint(500, 1000) * 10

#===================================================================================================

class Player(pygame.sprite.Sprite): # define this class before the infinite loop
    def __init__(self, initial_x, initial_y, topBoundary=0, bottomBoundary=HALF_HEIGHT):
        super(Player, self).__init__() # execute the __init__ method of the parent (Sprite object)
        self.surf = pygame.Surface((75, 25)) # create a surface <- our photonic ship
        self.surf.fill((PLAYER_COLOR)) # color of our photonic ship
        self.rect = self.surf.get_rect() # create a variable to access the surface as a rectangle

        self.rect.x = initial_x
        self.rect.y = initial_y

        self.topBoundary = topBoundary
        self.bottomBoundary = bottomBoundary
        self.leftBoundary = 0
        self.rightBoundary = SCREEN_WIDTH

        self.speed = INITIAL_PLAYER_SPEED

    def update(self, pressed_keys): # we move the rectangular with (x,y)
        if IN_SUPERPOSITION:
            speed = 0
        else:
            speed = self.speed

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT]:
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


class RegularPlayer(Player):
    def __init__(self, initial_x, initial_y, topBoundary=0, bottomBoundary=HALF_HEIGHT):
        super(RegularPlayer, self).__init__(initial_x, initial_y, topBoundary, bottomBoundary)

    def update(self, pressed_keys):
        super().update(pressed_keys)

    def flip(self):
        self.rect.y = (self.rect.y + HALF_HEIGHT) % SCREEN_HEIGHT
        if self.topBoundary == 0:
            self.topBoundary = HALF_HEIGHT
        else:
            self.topBoundary = 0
        if self.bottomBoundary == SCREEN_HEIGHT:
            self.bottomBoundary = HALF_HEIGHT
        else:
            self.bottomBoundary = SCREEN_HEIGHT

class TwinPlayer(Player):
    def __init__(self, initial_x, initial_y, topBoundary=0, bottomBoundary=HALF_HEIGHT):
        super(TwinPlayer, self).__init__(initial_x, initial_y, topBoundary, bottomBoundary)
        self.rect.y = (self.rect.y + HALF_HEIGHT) % SCREEN_HEIGHT
        if self.topBoundary == 0:
            self.topBoundary = HALF_HEIGHT
        else:
            self.topBoundary = 0
        if self.bottomBoundary == SCREEN_HEIGHT:
            self.bottomBoundary = HALF_HEIGHT
        else:
            self.bottomBoundary = SCREEN_HEIGHT

    def update(self, pressed_keys):
        super().update(pressed_keys)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10)) # Enemies are smaller than our photonic ship
        self.surf.fill((PLAYER_COLOR)) # the color of enemies - would you like to try different colors here?
        self.rect = self.surf.get_rect( # their positions are random but still they should appear on the right side
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), # position of x
                random.randint(0, SCREEN_HEIGHT), # position of y
            )
        )
        if IN_SUPERPOSITION:
            self.speed = random.randint(1,5) * ENEMY_MIN_SPEED
        else:
            self.speed = random.randint(1,4) * ENEMY_MAX_SPEED # we assign a random speed - how many pixel to move to the left in each frame

        self.in_superposition = False

    def update(self, pressed_keys):
        if not IN_SUPERPOSITION:
            self.rect.move_ip(-self.speed, 0)
            pass
        else:
            self.rect.move_ip(-self.speed, 0)
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -INITIAL_PLAYER_SPEED)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, INITIAL_PLAYER_SPEED)
            # Keep player on the screen
            if self.rect.top <= 0:
                self.rect.y = SCREEN_HEIGHT - 1
            elif self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.y = 0
        if self.rect.right < 0: # remove any enemy moveing out side of the screen
            self.kill() # a nice method inherited from Sprite()

    def updateSpeed(self, speed_const):
        self.speed = random.randint(1,5) * speed_const
        if speed_const == ENEMY_MAX_SPEED:
            self.in_superposition = False
        elif speed_const == ENEMY_MIN_SPEED:
            self.in_superposition = True

#===================================================================================================

def determinePlayerPosition(players):
    return random.choice(list(players))

def check_collision(players, enemies, start_time, screen, twin, current_player, all_sprites):
    global IN_SUPERPOSITION

    for player in players:
        if pygame.sprite.spritecollideany(player, enemies):

            if IN_SUPERPOSITION:        # Collision in superposition
                true_player = determinePlayerPosition(players)
                if true_player == player:       # Player got hit
                    print("Player got hit")
                    pass
                else:                           # Player survived
                    print("Player survived")
                    if player == twin:          # Twin survived
                        print("Twin survived")
                        players.remove(twin)
                        all_sprites.remove(twin)
                        twin.kill()
                        twin = None

                    else:                       # Regular player survived
                        print("Regular player survived")
                        players.remove(twin)
                        all_sprites.remove(twin)
                        twin.kill()
                        players.remove(current_player)
                        all_sprites.remove(current_player)
                        current_player.kill()
                        current_player = RegularPlayer(twin.rect.x, twin.rect.y, twin.topBoundary, twin.bottomBoundary)
                        players.add(current_player)
                        all_sprites.add(current_player)
                        twin = None

                    for enemy in enemies:
                        enemy.updateSpeed(ENEMY_MAX_SPEED)

                    for player in players:
                        player.speed = INITIAL_PLAYER_SPEED

                IN_SUPERPOSITION = not IN_SUPERPOSITION
                return True, False, twin, current_player

            time_total = time.time() - start_time
            minutes = int(time_total // 60)  # Get the whole minutes
            seconds = int(time_total % 60)   # Get the remaining seconds
            formatted_time = f"{minutes:02}:{seconds:02}"

            my_font = pygame.font.SysFont('Comic Sans MS', 28)
            text_surface = my_font.render(f"Game Over :( Time: {formatted_time}", False, (255, 255, 255), (BACKGROUND_COLOR))

            screen.blit(text_surface, (SCREEN_WIDTH/8, SCREEN_HEIGHT/2-text_surface.get_height()/2))

            for player in players:
                player.kill()
            return False, True, twin, current_player
    return True, False, twin, current_player

def main():
    global IN_SUPERPOSITION
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    # Add events
    pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)
    pygame.time.set_timer(NOT, NOT_TIME_INTERVAL)
    pygame.time.set_timer(HADAMARD, HADAMARD_TIME_INTERVAL)

    # Set players
    players = pygame.sprite.Group()
    current_player = RegularPlayer(0,0)
    players.add(current_player)

    # Set enemies
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(players)

    # Set flags
    start_time = time.time()
    twin = None
    running = True
    there_is_message = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == NOT:
                if not IN_SUPERPOSITION:
                    current_player.flip()
            elif event.type == HADAMARD:
                if IN_SUPERPOSITION:
                    players.remove(twin)
                    all_sprites.remove(twin)
                    twin.kill()
                    twin = None

                    for enemy in enemies:
                        enemy.updateSpeed(ENEMY_MAX_SPEED)

                    for player in players:
                        player.speed = INITIAL_PLAYER_SPEED

                else:
                    twin = TwinPlayer(current_player.rect.x, current_player.rect.y, topBoundary= current_player.topBoundary, bottomBoundary=current_player.bottomBoundary)
                    players.add(twin)
                    all_sprites.add(players)

                    for enemy in enemies:
                        enemy.updateSpeed(ENEMY_MIN_SPEED)

                    for player in players:
                        player.speed = 0

                IN_SUPERPOSITION = not IN_SUPERPOSITION

        screen.fill((BACKGROUND_COLOR))

        pressed_keys = pygame.key.get_pressed()

        players.update(pressed_keys)

        enemies.update(pressed_keys)

        running, there_is_message, twin, current_player = check_collision(players, enemies, start_time, screen, twin, current_player, all_sprites)

        if pressed_keys[K_ESCAPE]: running = False

        pygame.draw.line(screen, (255, 255, 255), (0, HALF_HEIGHT), (SCREEN_WIDTH, HALF_HEIGHT))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.flip() # show everything since the last frame
        clock.tick(30) # set the FPS rate

    if there_is_message: time.sleep(2) # sleep for 2 seconds

if __name__ == "__main__":
    main()
    pygame.quit()