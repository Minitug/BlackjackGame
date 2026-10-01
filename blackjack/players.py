from blackjack.cards import Hand

class Player:
    def __init__(self, name = "Player", balance = 1000):
        self.name = name
        self.hands = [Hand()]
        self.balance = balance
