from Games.Deck import Deck
from enum import Enum, unique, auto


class TexasHoldem:
    def __init__(self, players=list()):
        super().__init__()
        self.deck = Deck()
        self.players = players

    def addPLayer(self, player):
        self.players.append(player)

    @unique
    class Actions(Enum):
        CALL = auto()
        CHECK = auto()
        FOLD = auto()
        RAISE = auto()
