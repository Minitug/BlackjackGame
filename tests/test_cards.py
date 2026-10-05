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

from blackjack.cards import Card, Hand
from blackjack.players import Player
from blackjack.game import BlackjackGame


def make_hand(cards, bet=10):
    """Helper for quickly creating a specific hand."""
    hand = Hand(bet=bet)

    for suit, rank in cards:
        hand.add_card(Card(suit, rank))

    return hand


def test_different_players_can_have_different_bets():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.hands = [Hand(bet=100)]
    tug.hands = [Hand(bet=250)]

    assert mini.hands[0].bet == 100
    assert tug.hands[0].bet == 250


def test_one_player_bust_does_not_affect_other_player():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.hands = [
        make_hand([
            ("Hearts", "King"),
            ("Spades", "8"),
            ("Clubs", "5"),
        ])
    ]

    tug.hands = [
        make_hand([
            ("Hearts", "King"),
            ("Diamonds", "8"),
        ])
    ]

    assert mini.hands[0].bust
    assert not tug.hands[0].bust
    assert tug.hands[0].value == 18


def test_split_only_affects_correct_player():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.hands = [
        make_hand([
            ("Hearts", "8"),
            ("Spades", "8"),
        ], bet=50)
    ]

    tug.hands = [
        make_hand([
            ("Hearts", "King"),
            ("Spades", "7"),
        ], bet=100)
    ]

    game = BlackjackGame(
        players=[mini, tug],
        add_dealer=False
    )

    game.split_hand(mini, mini.hands[0])

    assert len(mini.hands) == 2
    assert len(tug.hands) == 1

    assert mini.hands[0].bet == 50
    assert mini.hands[1].bet == 50

    assert tug.hands[0].bet == 100


def test_both_players_can_split():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.hands = [
        make_hand([
            ("Hearts", "8"),
            ("Spades", "8"),
        ], bet=50)
    ]

    tug.hands = [
        make_hand([
            ("Clubs", "Queen"),
            ("Diamonds", "Queen"),
        ], bet=100)
    ]

    game = BlackjackGame(
        players=[mini, tug],
        add_dealer=False
    )

    game.split_hand(mini, mini.hands[0])
    game.split_hand(tug, tug.hands[0])

    assert len(mini.hands) == 2
    assert len(tug.hands) == 2

    assert mini.hands[0].bet == 50
    assert mini.hands[1].bet == 50

    assert tug.hands[0].bet == 100
    assert tug.hands[1].bet == 100


def test_double_down_only_changes_correct_hand():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.hands = [Hand(bet=100)]
    tug.hands = [Hand(bet=200)]

    mini.hands[0].bet *= 2
    mini.hands[0].double_down = True

    assert mini.hands[0].bet == 200
    assert mini.hands[0].double_down

    assert tug.hands[0].bet == 200
    assert not tug.hands[0].double_down


def test_player_can_stop_without_stopping_other_players():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.stop_playing()

    assert not mini.still_playing
    assert tug.still_playing

    assert any(player.still_playing for player in [mini, tug])


def test_no_players_still_playing():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    mini.stop_playing()
    tug.stop_playing()

    assert not any(
        player.still_playing
        for player in [mini, tug]
    )


def test_player_below_minimum_can_be_removed_independently():
    mini = Player(name="Mini", balance=5)
    tug = Player(name="Tug", balance=500)

    minimum_bet = 10

    if mini.balance < minimum_bet:
        mini.stop_playing()

    if tug.balance < minimum_bet:
        tug.stop_playing()

    assert not mini.still_playing
    assert tug.still_playing

def test_dealer_plays_if_one_player_busts_but_another_is_active():
    mini = Player(name="Mini", balance=1000)
    tug = Player(name="Tug", balance=1000)

    # Mini busts with 24
    mini.hands = [
        make_hand([
            ("Hearts", "King"),
            ("Spades", "8"),
            ("Clubs", "6"),
        ], bet=100)
    ]

    # Tug stands on 20
    tug.hands = [
        make_hand([
            ("Hearts", "King"),
            ("Diamonds", "Queen"),
        ], bet=100)
    ]
    tug.hands[0].stand = True

    game = BlackjackGame(players=[mini, tug])

    dealer_needs_to_play = any(
        not hand.bust
        and not hand.blackjack
        and not hand.surrender
        for player in game.players
        for hand in player.hands
    )

    assert mini.hands[0].bust
    assert not tug.hands[0].bust
    assert dealer_needs_to_play