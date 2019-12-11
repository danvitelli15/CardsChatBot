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
        return self.rank.value + " of " + self.suit.value

    def compareTo(self, card):
        return self.rank == card.rank and self.suit == card.suit


@unique
class Rank(Enum):
    ACE = "ace"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"


@unique
class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"
