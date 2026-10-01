from blackjack.cards import Deck, Hand
from blackjack.players import Player

class BlackjackGame:
    def __init__(self, players=[Player(name="Player"), Player(name="Dealer")], starting_balance=1000):
        self.players = []
        for player in players:
            if player.name == "Dealer":
                player.balance = float('inf')  # Dealer has infinite balance
            else:    
                player.balance = starting_balance
            
            self.players.append(player)
            self.choice = None

        self.deck = Deck()
        self.deck.shuffle()


    def play_round(self):

        for player in self.players:
            player.hands = []  # Reset hands for each player
            player.hands.append(Hand())

        for i in range(2):
            for player in self.players:
                player.hands[0].add_card(self.deck.draw_card())

        for player in self.players:
            for hand in player.hands:
                if hand.value == 21:
                    hand.blackjack = True
                    print(f"{player.name} has a blackjack!")
                    break
                if player.name != "Dealer":
                    print(f"{player.name}'s hand:")
                    hand.show_hand()
                    print(f"{player.name}'s hand value:", hand.value)
                    player.choice = input("Do you want to hit or stand? (H/S): ").upper()
                    while player.choice not in ['H', 'S']:
                        print("Invalid input. Please enter 'H' to hit or 'S' to stand.")
                        player.choice = input("Do you want to hit or stand? (H/S): ").upper()
                    while hand.value < 21 and player.choice != 'S':
                        if player.choice == 'H':
                            hand.add_card(self.deck.draw_card())
                            print(f"{player.name}'s hand:")
                            hand.show_hand()
                            # print(f"{player.name}'s hand value:", hand.value)
                            if hand.value > 21:
                                print(f"{player.name}'s hand busts!")
                                break
                            else:
                                # print(f"{player.name}'s hand value:", hand.value)
                                player.choice = input("Do you want to hit or stand? (H/S): ").upper()
                                while player.choice not in ['H', 'S']:
                                    print("Invalid input. Please enter 'H' to hit or 'S' to stand.")
                                    player.choice = input("Do you want to hit or stand? (H/S): ").upper()
                elif player.name == "Dealer" and not self.players[0].hands[0].bust:
                    print(f"Dealer's hand: {hand.value}, Player's hand: {self.players[0].hands[0].value}")
                    if hand.value < 17:
                        hand.add_card(self.deck.draw_card())
                        print(f"{player.name}'s hand:")
                        hand.show_hand()
                        print(f"{player.name}'s hand value:", hand.value)

        print(f"{self.players[0].name}'s final hand value:", self.players[0].hands[0].value)
        print(f"{self.players[1].name}'s final hand value:", self.players[1].hands[0].value)

        if (
            self.players[0].hands[0].bust
            or (
                self.players[1].hands[0].value > self.players[0].hands[0].value
                and not self.players[1].hands[0].bust
            )
):
            print(f"{self.players[1].name} wins!")
        elif self.players[0].hands[0].value > self.players[1].hands[0].value or self.players[1].hands[0].bust:
            print(f"{self.players[0].name} wins!")
        else:
            print("It's a tie!")