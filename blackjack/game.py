from blackjack.cards import Deck, Hand
from blackjack.players import Player

class BlackjackGame:
    def __init__(
        self,
        players=None,
        # dealer=None,
        starting_balance=1000,
        add_dealer=True,
        minimum_bet=10
    ):
        if players is None:
            players = [Player(name="Player")]
        else:
            players = list(players)

        if add_dealer:
            self.dealer = Player(name="Dealer", balance = float("inf"))

        self.players = []

        for player in players:
            player.balance = starting_balance

            self.players.append(player)

        self.choice = None
        self.minimum_bet = minimum_bet

        self.deck = Deck()
        self.deck.shuffle()


    def play_round(self):

        active_players = sum(player.still_playing for player in self.players)
        minimum_cards = active_players * 10 + 5

        # hand_index = 0
        if self.deck.cards_remaining() < minimum_cards:
            print("Reshuffling the deck...")
            self.deck.reset_deck()

        for player in self.players:
            player.hands = []
            player.hands.append(Hand())
        
        self.dealer.hands = []
        self.dealer.hands.append(Hand())

        self.place_bets()

        for i in range(2):
            for player in self.players + [self.dealer]:
                if player.still_playing:
                    player.hands[0].add_card(self.deck.draw_card())

        for player in self.players:
            hand_index = 0
            if player.still_playing:
                while hand_index < len(player.hands):
                    hand = player.hands[hand_index]
                    if hand.value == 21 and len(hand.cards) == 2 and not hand.split:
                        hand.blackjack = True
                        print(f"{player.name} has a blackjack!")
                        hand_index += 1
                        continue
                    # if player.name != "Dealer":
                    
                    split_occured = False
                    split_occured = self.play_player_turn(player, hand)

                    if split_occured:
                        continue

                    hand_index += 1

        self.play_dealer_turn()

        self.settle_bets()


    def get_player_choice(self, hand, balance):
        valid_choices = ['H', 'S']
        options = ["(H)it", "(S)tand"]

        if len(hand.cards) == 2:
            valid_choices.extend(['D'])
            options.extend(["(D)ouble down"])
            if not hand.split:
                valid_choices.append('R')
                options.append("Sur(R)ender")

        if hand.can_split():
            valid_choices.append('P')
            options.append("s(P)lit")



        choice_text = f"Do you want to {', '.join(options)}? ({'/'.join(valid_choices)}): "

        while True:
            choice = input(choice_text).upper()

            if choice in valid_choices:
                if choice == 'D' and balance < hand.bet * 2:
                    print("You don't have enough balance to double down. Please choose another option.")
                    continue
                elif choice == 'P' and balance < hand.bet * 2:
                    print("You don't have enough balance to split. Please choose another option.")
                    continue
                    
                return choice
            else:
                print(f"Invalid input. {choice_text}")


    def settle_bets(self):
        for player in self.players:
        # player = self.players[0]
        # dealer = self.players[1]

            if not player.still_playing:
                continue

            hands_to_settle = len(player.hands)
            # settled_hands = []
            winner_texts = []

            for hand in player.hands:
                # winning = 0
            # player_hand = player.hands[0]
                player_hand = hand
                dealer_hand = self.dealer.hands[0]

                # player_balance = self.players[0].balance

                winning_multiplier = 1

                if player_hand.blackjack and not dealer_hand.blackjack:
                    winning_multiplier = 1.5
                elif player_hand.surrender:
                    winning_multiplier = 0.5

                # print(f"{player.name}'s final hand value:", player_hand.value)
                # print(f"{dealer.name}'s final hand value:", dealer_hand.value)

                winnings = 0
                

                if (
                    player_hand.bust or player_hand.surrender
                    or (
                        dealer_hand.value > player_hand.value
                        and not dealer_hand.bust
                    )
                    ):
                    winnings -= player_hand.bet * winning_multiplier
                    winner_texts.append(f"Dealer wins! (-${abs(winnings):.2f})")
                    player.balance += winnings
                elif player_hand.value > dealer_hand.value or dealer_hand.bust:
                    winnings += player_hand.bet * winning_multiplier
                    winner_texts.append(f"{player.name} wins! (+${winnings:.2f})")
                    player.balance += winnings
                else:
                    winner_texts.append(f"{player.name} plays a tie!")

                # settled_hands.append()

            # hands_to_settle = 1

            if hands_to_settle == 1:
                print(winner_texts[0])
            else:
                settling_hand = 1
                for text in winner_texts:
                    print(f"{player.name}'s hand {settling_hand}: {text}")
                    settling_hand += 1
            print(f"{player.name}'s balance: ${player.balance:.2f}")
            if player.balance < self.minimum_bet:
                player.stop_playing()
            # player.calculate_winnings()

    def split_hand(self, player, hand):
        new_hand = Hand(bet=hand.bet, split=True)
        new_hand.add_card(hand.cards.pop())
        hand.calculate_value()
        new_hand.calculate_value()
        hand.add_card(self.deck.draw_card())
        new_hand.add_card(self.deck.draw_card())
        player.hands.append(new_hand)
        hand.split = True

    def play_player_turn(self, player, hand):
        print(f"{player.name}'s hand:")
        hand.show_hand()
        print(f"{player.name}'s hand value:", hand.value)

        while not hand.is_finished():
            player.choice = self.get_player_choice(hand, player.balance)
            if player.choice == 'R':
                hand.surrender = True
                print(f"{player.name} has surrendered.")
            elif player.choice == 'D':
                hand.double_down = True
                hand.bet *= 2
                print(f"{player.name} has doubled down.")
            elif player.choice == 'S':
                hand.stand = True
                print(f"{player.name} has chosen to stand.")
            elif player.choice == 'P':
                self.split_hand(player, hand)
                print(f"{player.name} has split their hand.")
                return True
                # split_occured = True
                # break  # Exit the loop to handle the new hand
                # continue
            
            if player.choice in ['H', 'D']:
                hand.add_card(self.deck.draw_card())
                print(f"{player.name}'s hand:")
                hand.show_hand()
            
        return False

    def play_dealer_turn(self):
        hand = self.dealer.hands[0]

        if any(
            not player_hand.bust
            and not player_hand.blackjack
            and not player_hand.surrender
            for player in self.players
            for player_hand in player.hands
        ):
            while not hand.is_finished() and hand.value < 17:
                hand.add_card(self.deck.draw_card())

            print("Dealer's hand:")
            hand.show_hand()
            print("Dealer's hand value:", hand.value)

    def place_bets(self):
        for player in self.players:
            if not player.still_playing:
                continue

            while True:
                print(
                    f"{player.name}, place your bet. "
                    f"Your balance is: {player.balance:.2f}. "
                    f"Bet 0 to leave table."
                )

                try:
                    bet = int(input().strip())
                except ValueError:
                    print("Invalid input. Number only.")
                    continue

                if bet == 0:
                    player.stop_playing()
                    break

                elif bet < self.minimum_bet:
                    print(f"Invalid input. Minimum bet is: {self.minimum_bet}")

                elif bet > player.balance:
                    print(f"Bet higher than balance. Your balance is: {player.balance:.2f}")

                else:
                    player.hands[0].bet = bet
                    break