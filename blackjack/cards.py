import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)

    def reset_deck(self):
        self.cards = []
        self.build_deck()
        self.shuffle()

                    
class Hand:
    def __init__(self, bet=0):
        self.cards = []
        self.value = 0
        self.bet = bet
        self.bust = False
        self.blackjack = False
        self.surrender = False
    
    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()
    
    def calculate_value(self):
        self.value = 0
        ace_count = 0
        for card in self.cards:
            if card.rank in ['Jack', 'Queen', 'King']:
                self.value += 10
            elif card.rank == 'Ace':
                self.value += 11
                ace_count += 1
            else:
                self.value += int(card.rank)
        
        while self.value > 21 and ace_count:
            self.value -= 10
            ace_count -= 1

        if self.value > 21:
            self.bust = True
        
        return self.value

    def show_hand(self):
        for card in self.cards:
            print(card)
        print("Hand value:", self.value)
