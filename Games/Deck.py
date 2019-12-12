from enum import Enum, auto, unique
from random import shuffle


class Deck:
    def __init__(self):
        super().__init__()
        self.cards = list()
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        self.cards.clear()
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)

    def toString(self):
        result = ""
        for card in self.cards:
            result = result + card.toString() + "\n"
        return result


class Card:
    def __init__(self, rank, suit):
        super().__init__()
        self.rank = rank
        self.suit = suit

    def toString(self):
        return self.rank.getName() + " of " + self.suit.value

    def equals(self, card):
        return self.rank == card.rank and self.suit == card.suit

    def compareTo(self, card):
        return self.rank - card.rank

@unique
class Rank(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

    def getName(self):
        names = {
            0: "two",
            1: "three",
            2: "four",
            3: "five",
            4: "six",
            5: "seven",
            6: "eight",
            7: "nine",
            8: "ten",
            9: "jack",
            10: "queen",
            11: "king",
            12: "ace"
        }
        return names[self.value]

@unique
class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"
