from enum import Enum as enum


class SwapState(enum):
    SWAP = 0
    NO_SWAP = 1

class SuperpositionState(enum):
    SUPERPOSITION = 0
    NO_SUPERPOSITION = 1

class State:
    def __init__(self):
        self.superposition_state = SuperpositionState.NO_SUPERPOSITION
        self.swap_state = SwapState.NO_SWAP
        self.lives = 3
        self.score = 0