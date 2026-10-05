from blackjack.game import BlackjackGame
from blackjack.players import Player

def show_winnings(game):
    for player in game.players:
        player.calculate_winnings()
        if player.winnings > 0:
            print(f"{player.name} won ${player.winnings:.2f}!")
        elif player.winnings < 0:
            print(f"{player.name} lost ${-player.winnings:.2f}.")
        else:
            print("{player.name} broke even.")
        # break


print("Welcome to Blackjack!")
print("You start with a balance of $1000.")
print("You win by leaving the table with more money than you started with.")
print("Do you want to play against a (D)ealer (up to 5 players) or 1v1 in (P)vP? (D/P)")
gamemode = ""
while True:
    gamemode = input().strip().lower()
    if gamemode == 'd':
        print("You've chosen to play against the dealer")
        print("How many players do you want to enter the game?")
        
        players_input = input().strip()
        try:
            number_of_players = int(players_input)
        except ValueError:
            print("Invalid input. Setting number of players to 1")
            number_of_players = 1
        
        break

    elif gamemode == 'p':
        print("You've chosen to play 1v1 head to head")
        number_of_players = 2
        break

    else:
        print("You must enter D for dealer, or P for PvP")

# player_to_enter = 1
unnamed_players = 1
players_to_add = []
for i in range(number_of_players):
    print(f"What is the name of player {i+1}?")
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

if gamemode == 'd':
    game = BlackjackGame(new_players)

else:
    game = BlackjackGame(players = new_players, add_dealer = False, minimum_bet = 0)

# winnings = 0

while True:
    if any(player.still_playing for player in game.players):
        print("Do you want to play a round of blackjack? (Y/N)")
        choice = input().strip().lower()
        if choice == 'y':
            if gamemode == 'd':
                game.play_round_against_dealer()
            else:
                game.play_round_pvp()
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

