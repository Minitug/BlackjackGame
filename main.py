from blackjack.game import BlackjackGame
from blackjack.players import Player

def show_winnings(game):
    for player in game.players:
        player.calculate_winnings()
        # winnings = game.players[0].balance - 1000
        if player.winnings > 0:
            print(f"{player.name} won ${player.winnings:.2f}!")
        elif player.winnings < 0:
            print(f"{player.name} lost ${-player.winnings:.2f}.")
        else:
            print("{player.name} broke even.")
        # break



print("Welcome to Blackjack!")
print("You start with a balance of $1000.")
print("You win by leaving the table with more money, than you started with.")
print("How many players do you want to enter the game?")
players_input = input().strip()

try:
    number_of_players = int(players_input)
except ValueError:
    print("Invalid input. Setting number of players to 1")
    number_of_players = 1

unnamed_players = 1
players_to_add = []
for i in range(number_of_players):
    print("What is the name of the player?")
    name = input().strip()
    if not name or name.isspace() or name.lower() == "dealer":
        print("Invalid name. Setting name to 'Player'.")
        name = "Player " + unnamed_players
        unnamed_players += 1
    players_to_add.append(name)
    print(f"Good luck, {name}!")

new_players = []
for player in players_to_add:
    new_players.append(Player(name=player))
game = BlackjackGame(new_players)
    
# winnings = 0

while True:
    if any(player.still_playing for player in game.players):
        print("Do you want to play a round of blackjack? (Y/N)")
        choice = input().strip().lower()
        if choice == 'y':
            # print(f"Your current balance is: ${game.players[0].balance}")
            # print(f"Place your bet for the next round (minimum bet is ${game.minimum_bet}):")
            # choice = input().strip()
            # try:
            #     bet = int(choice)
            # except ValueError:
            #     print(f"Invalid input. Setting bet to minimum: ${game.minimum_bet}.")
            #     bet = game.minimum_bet
            # if bet < game.minimum_bet:
            #     print(f"Bet must be at least ${game.minimum_bet}. Setting bet to minimum.")
            #     bet = game.minimum_bet
            # elif bet > game.players[0].balance:
            #     print("You don't have enough balance for that bet. Setting bet to your current balance.")
            #     bet = game.players[0].balance
            game.play_round()
        elif choice != 'n':
            print("Invalid input. Please enter 'Y' or 'N'.")
        else:
            print("Thanks for playing!")
            show_winnings(game)
            break
    else:
        print("Everyone has left the table. Thank you for playing.")
        show_winnings(game)
        break

