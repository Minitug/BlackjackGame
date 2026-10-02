from blackjack.players import Player
from blackjack.cards import Hand, Card, Deck
from blackjack.game import BlackjackGame
import pytest

def test_player_get_split():
    # Create a mock player and hand with two cards of the same rank
    player = Player(name="Test Player", balance=100)
    hand = Hand(bet=10)
    hand.add_card(Card('Hearts', '8'))
    hand.add_card(Card('Diamonds', '8'))
    player.hands.append(hand)

    # Check if the player can split
    assert hand.can_split(), "Player should be able to split with two cards of the same rank."

    # Now test with two cards of different ranks
    hand2 = Hand(bet=10)
    hand2.add_card(Card('Hearts', '8'))
    hand2.add_card(Card('Diamonds', '9'))
    player.hands.append(hand2)

    # Check if the player cannot split
    assert not hand2.can_split(), "Player should not be able to split with two cards of different ranks."

def test_ace_changes_from_11_to_1():
    hand = Hand()
    hand.add_card(Card("Hearts", "Ace"))
    hand.add_card(Card("Spades", "9"))
    hand.add_card(Card("Clubs", "5"))

    assert hand.value == 15
    assert not hand.bust

def test_multiple_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "Ace"))
    hand.add_card(Card("Spades", "Ace"))
    hand.add_card(Card("Clubs", "9"))

    assert hand.value == 21


def test_draw_reduces_deck_size():
    deck = Deck()

    assert deck.cards_remaining() == 52

    deck.draw_card()

    assert deck.cards_remaining() == 51

def test_three_cards_cannot_split():
    hand = Hand()
    hand.add_card(Card("Hearts", "8"))
    hand.add_card(Card("Diamonds", "8"))
    hand.add_card(Card("Clubs", "8"))

    assert not hand.can_split()


def test_split_hand():
    # Create a mock player and hand with two cards of the same rank
    player = Player(name="Test Player", balance=100)
    hand = Hand(bet=50)
    hand.add_card(Card("Hearts", "8"))
    hand.add_card(Card("Diamonds", "8"))
    player.hands.append(hand)

    # Simulate splitting the hand
    game = BlackjackGame(players=[player], add_dealer=False)
    game.split_hand(player, hand)

    # Check if the hand was split correctly
    assert len(player.hands) == 2
    assert len(player.hands[0].cards) == 2
    assert len(player.hands[1].cards) == 2
    assert player.hands[0].bet == 50
    assert player.hands[1].bet == 50
    assert player.hands[0].cards[0].rank == "8"
    assert player.hands[1].cards[0].rank == "8"

    cards_before = game.deck.cards_remaining()

    game.split_hand(player, hand)

    assert game.deck.cards_remaining() == cards_before - 2