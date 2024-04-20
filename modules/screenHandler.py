import pygame
from modules.state import State, SuperpositionState

"""
boundaries
fill
draw_line
blit
screen
"""

class ScreenHandler(pygame.sprite.Sprite):
    def __init__(self, width, height, background_color, state):
        super().__init__()
        self.top = 0
        self.bot = height
        self.left = 0
        self.right = width
        self.half_height = height // 2
        self.half_width = width // 2
        self.background_color = background_color
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = state
        self.active_messages = []
        self.message_timespan = 2500
        self.my_font = pygame.font.SysFont('Comic Sans MS', 28)  # Create font object once

    def fill(self):
        color = (0, 0, 0) if self.state.superposition_state == SuperpositionState.SUPERPOSITION else self.background_color
        self.screen.fill(color)

    def draw_line(self, color, start, end):
        pygame.draw.line(self.screen, color, start, end)

    def blit(self, entity):
        self.screen.blit(entity.surf, entity.rect)

    def update(self, _pressed_keys):
        current_time = pygame.time.get_ticks()  # Get the current time once per frame
        self.draw_line((255, 255, 255), (0, self.half_height), (self.right, self.half_height))

        # Display and update message handling
        self.active_messages = [msg for msg in self.active_messages if current_time < msg[3] + self.message_timespan]
        for message in self.active_messages:
            self.print_message(message[0], message[1], message[2])

        # Display lives and score
        self.print_message(f"Lives: {self.state.lives}", 10, 10)
        self.print_message(f"Score: {self.state.score}", 10, 40)

        self.clock.tick(30)

    def print_message(self, message, x, y):
        text_surface = self.my_font.render(message, False, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def add_message(self, message, x, y):
        self.active_messages.append((message, x, y, pygame.time.get_ticks()))  # Store current tick count
