from blackjack.cards import Deck, Hand
from blackjack.players import Player
from blackjack.game import BlackjackGame


game = BlackjackGame()

while True:
    print("Do you want to play a round of blackjack? (Y/N)")
    choice = input().strip().lower()
    if choice == 'y':
        game.play_round()
    elif choice != 'n':
        print("Invalid input. Please enter 'Y' or 'N'.")
    else:
        print("Thanks for playing!")
        break