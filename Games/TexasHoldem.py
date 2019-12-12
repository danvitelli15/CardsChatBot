from Games.Deck import Deck
from Game.Player import Player
from enum import Enum, unique, auto


class TexasHoldem:
    BUTTON = "button"
    SMALL_BLIND = "smallBlind"
    BIG_BLIND = "bigBlind"

    def __init__(self, players=list()):
        super().__init__()
        self.deck = Deck()
        self.players = players
        self.roles = {BUTTON: 0, SMALL_BLIND: 1, BIG_BLIND: 2}

    def addPLayer(self, player: Player):
        self.players.append(player)

    def round(self):
        return

    @unique
    class Actions(Enum):
        CALL = auto()
        CHECK = auto()
        FOLD = auto()
        RAISE = auto()

    @unique
    class Hands(Enum):
        HIGH_CARD = 0
        PAIR = 1
        TWO_PAIR = 2
        THREE_OF_A_KIND = 3
        STRAIGHT = 4
        FLUSH = 5
        FULL_HOUSE = 6
        FOUR_OF_A_KIND = 7
        STRAIGHT_FLUSH = 8
        ROYAL_FLUSH = 9
