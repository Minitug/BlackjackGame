from blackjack.cards import Card, Deck, Hand

deck = Deck()
deck.shuffle()
# for card in deck.cards:
#     print(card.suit, card.rank)
playerhand = Hand()
dealerhand = Hand()
playerhand.add_card(deck.draw_card())
dealerhand.add_card(deck.draw_card())
playerhand.add_card(deck.draw_card())
dealerhand.add_card(deck.draw_card())
print("Player's hand:")
for card in playerhand.cards:
    print(card.suit, card.rank)
print("Player hand value:", playerhand.value)
print("Dealer's hand:")
for card in dealerhand.cards:
    print(card.suit, card.rank)
print("Dealer hand value:", dealerhand.value)

if playerhand.value > 21:
    print("Player busts - dealer wins!")
elif dealerhand.value > 21:
    print("Dealer busts - player wins!")
elif dealerhand.value > playerhand.value:
    print("Dealer wins!")
elif playerhand.value > dealerhand.value:
    print("Player wins!")
else:
    print("Push!")