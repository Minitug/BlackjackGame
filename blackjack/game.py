from blackjack.cards import Deck, Hand
from blackjack.players import Player
from enum import Enum

class GameState(Enum):
    LOBBY = "Lobby"
    BETTING = "Betting"
    PLAYING = "Playing"
    ROUND_END = "Round End"

class BlackjackGame:
    def __init__(
        self,
        players=None,
        starting_balance=1000,
        add_dealer=True,
        minimum_bet=10,
        start_as_lobby=False
    ):
        if players is None and not start_as_lobby:
            players = [Player(name="Player")]
        else:
            players = list(players)

        self.add_dealer = add_dealer

        if add_dealer:
            self.dealer = Player(name="Dealer", balance = float("inf"))

        self.players = []

        for player in players:
            player.balance = starting_balance

            self.players.append(player)

        self.head_to_head_first_player = 0
        self.minimum_bet = minimum_bet

        self.deck = Deck()
        self.deck.shuffle()

        if start_as_lobby:
            self.game_state = GameState.LOBBY
        else:
            self.game_state = GameState.BETTING

        self.host_id = ""

        self.current_player_index = 0
        self.current_hand_index = 0




    def play_round_against_dealer(self):

        self.new_round()

        self.place_bets()

        self.deal_initial_cards()

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
        valid_choices, options = self.get_valid_actions(hand, balance)

        choice_text = f"Do you want to {', '.join(options)}? ({'/'.join(valid_choices)}): "

        while True:
            choice = input(choice_text).upper()

            if choice in valid_choices:
                return choice
            
            print(f"Invalid input. {choice_text}")


    def get_valid_actions(self, hand, balance):
        valid_choices = ['H', 'S']
        options = ["(H)it", "(S)tand"]

        if self.dealer:  
            if len(hand.cards) == 2:
                valid_choices.extend(['D'])
                options.extend("(D)ouble down")
                if not hand.split:
                    valid_choices.append('R')
                    options.append("Sur(R)ender")

            if hand.can_split():
                valid_choices.append('P')
                options.append("s(P)lit")

            if balance < hand.bet * 2:
                if 'D' in valid_choices:
                    valid_choices.remove('D')
                    options.remove("(D)ouble down")
                if 'P' in valid_choices:
                    valid_choices.remove('P')
                    options.remove("Sur(R)ender")

        return valid_choices, options


    def settle_bets(self):
        for player in self.players:

            if not player.still_playing:
                continue

            hands_to_settle = len(player.hands)
            # settled_hands = []
            winner_texts = []

            for hand in player.hands:
                player_hand = hand
                dealer_hand = self.dealer.hands[0]

                winning_multiplier = 1

                if player_hand.blackjack and not dealer_hand.blackjack:
                    winning_multiplier = 1.5
                elif player_hand.surrender:
                    winning_multiplier = 0.5

                winnings = 0
                

                if (
                    player_hand.bust or player_hand.surrender
                    or (
                        dealer_hand.value > player_hand.value
                        and not dealer_hand.bust
                    )
                    or (
                        dealer_hand.blackjack
                        and not player_hand.blackjack
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
            action = self.get_player_choice(hand, player.balance)
            action_result, action_message = self.perform_player_action(player, hand, action)
            print(action_message)

            if not action_result:
                continue

            if action == 'P':
                return True

            print(f"{player.name}'s hand:")
            hand.show_hand()
            print(f"{player.name}'s hand value:", hand.value)
            
        return False

    def perform_player_action(self, player, hand, action):
        valid_actions, options = self.get_valid_actions(hand, player.balance)
        if action not in valid_actions:
            return False, "Invalid action"

        if action == 'R':
            hand.surrender = True
            message = (f"{player.name} has surrendered.")
        elif action == 'D':
            hand.double_down = True
            hand.bet *= 2
            message = (f"{player.name} has doubled down.")
        elif action == 'S':
            hand.stand = True
            message = (f"{player.name} has chosen to stand.")
        elif action == 'P':
            self.split_hand(player, hand)
            message = (f"{player.name} has split their hand.")
            
        if action in ['H', 'D']:
            hand.add_card(self.deck.draw_card())

            if action == 'H':
                message = f"{player.name} has hit."

        return True, message

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

                success, message = self.place_bet(player, bet)

                if success:
                    break

                print(message)

                

    def place_bet(self, player, bet):
        if bet == 0:
            player.stop_playing()
            return True, "Player left the table"

        elif bet < self.minimum_bet:
            message = f"Invalid input. Minimum bet is: {self.minimum_bet}"
            return False, message

        elif bet > player.balance:
            message = f"Bet higher than balance. Your balance is: {player.balance:.2f}"
            return False, message

        else:
            player.hands[0].bet = bet
            return True, "Bet Accepted"


    def play_round_pvp(self):
        self.new_round()

        player1 = self.players[self.head_to_head_first_player]
        self.head_to_head_first_player = 1 - self.head_to_head_first_player
        player2 = self.players[self.head_to_head_first_player]

        maximum_bet = min(player1.balance, player2.balance)

        while True:
            print(
                f"{player1.name}, place your bet. "
                f"{player1.name} balance is: {player1.balance:.2f}. "
                f"{player2.name} balance is: {player2.balance:.2f}. "
            )

            try:
                bet = int(input().strip())
            except ValueError:
                print("Invalid input. Number only.")
                continue

            if bet > maximum_bet:
                print(f"Invalid input. Maximum bet is: {maximum_bet}")

            else:
                break

        for i in range(2):
            for player in self.players:
                if player.still_playing:
                    player.hands[0].add_card(self.deck.draw_card())

        for player in [player1, player2]:
            if player.hands[0].value == 21 and len(player.hands[0].cards) == 2:
                player.hands[0].blackjack = True
                print(f"{player.name} has a blackjack!")
                continue

        if not player1.hands[0].blackjack and not player2.hands[0].blackjack:
            for player in [player1, player2]:
                self.play_player_turn(player, player.hands[0])

        winner = None
        loser = None

        if player1.hands[0].bust or player2.hands[0].bust:
            if player1.hands[0].bust and player2.hands[0].bust:
                print("What are you both doing? It's a tie")
            elif player1.hands[0].bust:
                print(f"{player2.name} wins! {bet}")
                winner = player2
                loser = player1
            else:
                print(f"{player1.name} wins! {bet}")
                winner = player1
                loser = player2

        elif player1.hands[0].value > player2.hands[0].value:
            print(f"{player1.name} wins! {bet}")
            winner = player1
            loser = player2

        elif player1.hands[0].value < player2.hands[0].value:
            print(f"{player2.name} wins! {bet}")
            winner = player2
            loser = player1

        else:
            print("It's a tie")

        if winner:
            winner.balance += bet
            loser.balance -= bet 


    def new_round(self):
        active_players = sum(player.still_playing for player in self.players)
        minimum_cards = active_players * 10 + 5

        if self.deck.cards_remaining() < minimum_cards:
            print("Reshuffling the deck...")
            self.deck.reset_deck()

        for player in self.players:
            player.hands = []
            player.hands.append(Hand())

        if self.dealer:
            self.dealer.hands = []
            self.dealer.hands.append(Hand())




    def all_players_bet(self):
        return all(
            player.hands[0].bet is not None
            for player in self.players
            if player.still_playing
        )

    def deal_initial_cards(self):
        for i in range(2):
            for player in self.players + [self.dealer]:
                if player.still_playing:
                    player.hands[0].add_card(self.deck.draw_card())