from blackjack.game import BlackjackGame
from blackjack.players import Player

print("Welcome to Blackjack!")
print("You start with a balance of $1000.")
print("In the current version, you're playing one on one against the dealer.")
print("You win by leaving the table with more money, than you started with.")
print("What is your name?")
name = input().strip()
if not name or name.isspace() or name.lower() == "dealer":
    print("Invalid name. Setting name to 'Player'.")
    name = "Player"
print(f"Good luck, {name}!")

game = BlackjackGame([Player(name=name)])
    
winnings = 0

while True:
    if game.players[0].balance >= game.minimum_bet:
        print("Do you want to play a round of blackjack? (Y/N)")
        choice = input().strip().lower()
        if choice == 'y':
            print(f"Your current balance is: ${game.players[0].balance}")
            print(f"Place your bet for the next round (minimum bet is ${game.minimum_bet}):")
            choice = input().strip()
            try:
                bet = int(choice)
            except ValueError:
                print(f"Invalid input. Setting bet to minimum: ${game.minimum_bet}.")
                bet = game.minimum_bet
            if bet < game.minimum_bet:
                print(f"Bet must be at least ${game.minimum_bet}. Setting bet to minimum.")
                bet = game.minimum_bet
            elif bet > game.players[0].balance:
                print("You don't have enough balance for that bet. Setting bet to your current balance.")
                bet = game.players[0].balance
            game.play_round(bet)
        elif choice != 'n':
            print("Invalid input. Please enter 'Y' or 'N'.")
        else:
            print("Thanks for playing!")
            winnings = game.players[0].balance - 1000
            if winnings > 0:
                print(f"You won ${winnings}!")
            elif winnings < 0:
                print(f"You lost ${-winnings}.")
            else:
                print("You broke even.")
            break
    else:
        print("You don't have enough balance to continue playing. Game over.")
        winnings = game.players[0].balance - 1000
        if winnings > 0:
            print(f"You won ${winnings}!")
        elif winnings < 0:
            print(f"You lost ${-winnings}.")
        else:
            print("You broke even.")
        break