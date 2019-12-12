from Deck import Deck
from Player import Player, Hand
from enum import Enum, unique, auto


class TexasHoldem:
    BUTTON = "button"
    SMALL_BLIND = "smallBlind"
    BIG_BLIND = "bigBlind"

    def __init__(self, players=list(), smallBlind=.5, bigBlind=1):
        super().__init__()
        self.deck = Deck()
        self.players = players
        self.roles = {BUTTON: 0, SMALL_BLIND: 0, BIG_BLIND: 0}
        self.smallBlindBet = smallBlind
        self.bigBlindBet = bigBlind
        self.pot = 0
        self.tableCards = Hand()

    def addPLayer(self, player: Player):
        self.players.append(player)

    def hand(self):
        self.newHand()
        self.dealHand()
        self.payBlinds()
        self.bettingRounds()

        return

    def round(self):
        return False

    def bettingRounds(self):
        anoutherRound = True
        while anoutherRound:
            anoutherRound = self.round()

    def payBlinds(self):
        self.pot += self.players[self.roles[SMALL_BLIND]
                                 ].bet(self.smallBlindBet)
        self.pot += self.players[self.roles[BIG_BLIND]].bet(self.bigBlindBet)

    def newHand(self):
        self.deck.shuffle()
        self.pot = 0

        self.roles[BUTTON] = self.nextPlayer(self.roles[BUTTON])
        self.roles[SMALL_BLIND] = self.nextPlayer(self.roles[BUTTON])
        self.roles[BIG_BLIND] = self.nextPlayer(self.roles[SMALL_BLIND])

    def dealHand(self):
        for i in range(2):
            for player in self.players:
                player.draw(self.deck.draw())

    def nextPlayer(self, playerIndex):
        return 0 if playerIndex >= len(self.players) else playerIndex + 1


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
