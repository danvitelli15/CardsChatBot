from Games.Deck import Card


class Player:
    def __init__(self, name, buyIn):
        super().__init__()
        self.name = name
        self.hand = Hand()
        self.money = buyIn

    def bet(self, amount):
        if amount < self.money:
            self.money -= amount
        else:
            self.money = 0
        return self.money

    def draw(self, card):
        return self.hand.draw(card)

    def win(self, amount):
        self.money += amount
        return self.money

    def toString(self):
        return "[" + self.name + ": hand: " + self.hand.toString + ", money: $" + self.money + "]"

    class Hand:
        def __init__(self, cards=list()):
            super().__init__()
            self.cards = cards

        def draw(self, card: Card):
            self.cards.append(card)
            return self.cards

        def discard(self):
            self.cards.clear()
            return self.cards

        def order(self):
            if len(self.cards) > 1:
                for j in range(len(self.cards)):
                    card = self.cards.pop(0)
                    index = 0
                    for i in range(len(self.cards)):
                        if self.cards[i].rank < card.rank:
                            index = i
                    self.cards.insert(index, card)
            return self.cards

        def toString(self):
            cardStr = ""
            for card in self.cards:
                cardStr += card.toString() + ", "
            return "Hand: [" + cardStr[:-2] + "]"
