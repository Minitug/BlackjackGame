from blackjack.cards import Deck, Hand
from blackjack.players import Player

class BlackjackGame:
    def __init__(
        self,
        players=None,
        starting_balance=1000,
        add_dealer=True,
        minimum_bet=10
    ):
        if players is None:
            players = [Player(name="Player")]
        else:
            players = list(players)

        if add_dealer:
            players.append(Player(name="Dealer"))

        self.players = []

        for player in players:
            if player.name == "Dealer":
                player.balance = float("inf")
            else:
                player.balance = starting_balance

            self.players.append(player)

        self.choice = None
        self.minimum_bet = minimum_bet

        self.deck = Deck()
        self.deck.shuffle()


    def play_round(self, bet):
        if self.deck.cards_remaining() < 15:
            print("Reshuffling the deck...")
            self.deck.reset_deck()

        for player in self.players:
            player.hands = []  # Reset hands for each player
            player.hands.append(Hand())

        for i in range(2):
            for player in self.players:
                player.hands[0].add_card(self.deck.draw_card())

        for player in self.players:
            for hand in player.hands:
                if hand.value == 21 and len(hand.cards) == 2:
                    hand.blackjack = True
                    print(f"{player.name} has a blackjack!")
                    continue
                if player.name != "Dealer":
                    print(f"{player.name}'s hand:")
                    hand.show_hand()
                    print(f"{player.name}'s hand value:", hand.value)
                    while not hand.is_finished():
                        player.choice = self.get_player_choice(hand, player.balance)
                        if player.choice in ['H', 'D']:
                            hand.add_card(self.deck.draw_card())
                            print(f"{player.name}'s hand:")
                            hand.show_hand()
                        if player.choice == 'R':
                            hand.surrender = True
                            print(f"{self.players[0].name} has surrendered.")
                        elif player.choice == 'D':
                            hand.double_down = True
                            print(f"{self.players[0].name} has doubled down.")
                        elif player.choice == 'S':
                            hand.stand = True
                            print(f"{self.players[0].name} has chosen to stand.")
                elif (
                    player.name == "Dealer"
                    and not self.players[0].hands[0].bust
                    and not self.players[0].hands[0].blackjack
                    and not self.players[0].hands[0].surrender
                    ):
                    print(f"Dealer's hand: {hand.value}, {self.players[0].name}'s hand: {self.players[0].hands[0].value}")
                    while not hand.is_finished() and hand.value < 17:
                    # if hand.value < 17:
                        hand.add_card(self.deck.draw_card())
                        print(f"{player.name}'s hand:")
                        hand.show_hand()
                        print(f"{player.name}'s hand value:", hand.value)

        print(f"{self.players[0].name}'s final hand value:", self.players[0].hands[0].value)
        print(f"{self.players[1].name}'s final hand value:", self.players[1].hands[0].value)

        self.settle_bets(bet)


    def get_player_choice(self, hand, balance):
        valid_choices = ['H', 'S', 'R', 'D']  # H: Hit, S: Stand, R: Surrender, D: Double Down

        while True:
            choice = input("Do you want to (H)it, (S)tand, sur(R)ender or (D)ouble down (H/S/R/D): ").upper()

            if choice in valid_choices:
                if len(hand.cards) > 2:
                    if choice == 'R':
                        print("You can only surrender on your first two cards. Please choose another option.")
                        continue
                    elif choice == 'D':
                        print("You can only double down on your first two cards. Please choose another option.")
                        continue
                if choice == 'D' and balance < hand.bet * 2:
                    print("You don't have enough balance to double down. Please choose another option.")
                    continue
                    
                return choice
            else:
                print("Invalid input. Please enter 'H' to hit, 'S' to stand, 'R' to surrender or 'D' to double down.")


    def settle_bets(self, bet):
        player = self.players[0]
        dealer = self.players[1]

        player_hand = player.hands[0]
        dealer_hand = dealer.hands[0]

        # player_balance = self.players[0].balance

        winning_multiplier = 1
        bet_multiplier = 1

        if player_hand.blackjack and not dealer_hand.blackjack:
            winning_multiplier = 1.5
        elif player_hand.surrender:
            winning_multiplier = 0.5
        
        if player_hand.double_down:
            bet_multiplier = 2

        if (
            player_hand.bust or player_hand.surrender
            or (
                dealer_hand.value > player_hand.value
                and not dealer_hand.bust
            )
            ):
            print(f"{dealer.name} wins!")
            player.balance -= bet * winning_multiplier * bet_multiplier
        elif player_hand.value > dealer_hand.value or dealer_hand.bust:
            print(f"{player.name} wins!")
            player.balance += bet * winning_multiplier * bet_multiplier
        else:
            print("It's a tie!")

        print(f"{player.name}'s balance: ${player.balance}")