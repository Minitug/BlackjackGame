import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from blackjack.players import Player
from blackjack.game import BlackjackGame, GameState

class PlayerRequest(BaseModel):
    name: str

class PlayerIdRequest(BaseModel):
    player_id: str

class PlayerBet(BaseModel):
    player_id: str
    bet_value: int

class PlayerAction(BaseModel):
    player_id: str
    action: str

def find_player_through_id(request_player_id):
    found_player = None
    for player in game.players:
            if player.player_id == request_player_id:
                found_player = player
                break

    return found_player

app = FastAPI()

game = None
players = []

game = BlackjackGame(
    players=[],
    start_as_lobby=True
    )

@app.get("/hello")
def hello():
    message = (
    "Welcome to Blackjack!"
    "\nYou start with a balance of $1000."
    "\nYou win by leaving the table with more money than you started with."
    # "\nDo you want to play against a (D)ealer (up to 5 players) or 1v1 in (P)vP? (D/P)"
    )
    return{"message": message}


@app.post("/game/start")
def start_game(request: PlayerIdRequest):

    found_player = find_player_through_id(request.player_id)

    if request.player_id == game.host_id:
        game.game_state = GameState.BETTING
        game.new_round()

    return {
        "message": "Game created",
        "state": game.game_state.value
    }


@app.get("/game/state")
def get_game_state():
    if game is None:
        return{"error": "No game has been started"}

    message = ""
    waiting_players_to_bet = []
    waiting_for_players_ids = []
    valid_choices = []
    options = []
    dealer_hand = {}

    if game.game_state == GameState.BETTING:
        all_players_bet = all(
            player.hands[0].bet is not None
            for player in game.players
        )

        for player in game.players:
            print(
                f"Player: {player.name}, "
                f"Bet: {player.hands[0].bet}, "
                f"Type: {type(player.hands[0].bet)}"
            )

        if not all_players_bet:
            for player in game.players:
                if player.hands[0].bet is None:
                    waiting_players_to_bet.append(player.name)
                    waiting_for_players_ids.append(player.player_id)
            message = "Waiting for players: " + ", ".join(waiting_players_to_bet) + "."

    if game.game_state == GameState.PLAYING:
        player = game.players[game.current_player_index]
        hand = player.hands[game.current_hand_index]
        is_blackjack = game.test_blackjack(hand)
        balance = player.balance
        if not is_blackjack:
            valid_choices, options = game.get_valid_actions(hand, balance)
        message = f"{player.name} is playing their turn."
        waiting_for_players_ids.append(player.player_id)

    if game.game_state == GameState.ROUND_END:
        dealer_hand = game.dealer.hands[0]

    return {
        "game_state": game.game_state,
        "minimum_bet": game.minimum_bet,
        "cards_remaining": game.deck.cards_remaining(),
        "players": [
            {
                "name": player.name,
                "balance": player.balance,
                "hands": player.hands

            }
            for player in game.players
        ],
        "dealer_hand": dealer_hand,
        "message": message,
        "players_missing_actions": waiting_for_players_ids,
        "valid_choices": valid_choices,
        "options": options
    }

@app.post("/player/add")
def add_player(request: PlayerRequest):
    player_id = str(uuid.uuid4())
    player = Player(name=request.name, player_id=player_id)
    is_host = len(game.players) == 0

    message = f"{player.name} joined the game."

    if is_host:
        game.host_id = player_id
        # player_is_host = True
        message += " They're given host priveleges."

    game.players.append(player)

    return {
        "message": message,
        "player_id": player_id,
        "name": player.name,
        "balance": player.balance,
        "is_host": is_host
    }


@app.post("/player/bet")
def player_bet(request: PlayerBet):
    found_player = None
    found_player = find_player_through_id(request.player_id)

    if found_player == None:
        return {"message": "Player was not found"}

    found_player.hands[0].bet = request.bet_value

    success, message = game.place_bet(found_player, request.bet_value)

    if success and game.all_players_bet():
        game.game_state = GameState.PLAYING
        game.deal_initial_cards()
        


    return {
        "success": success,
        "message": message
        }


@app.get("/player/{player_id}/hand")
def get_player_hand(player_id: str):
    found_player = find_player_through_id(player_id)

    if found_player == None:
        return {
            "success": False,
            "message": "It's not your turn."
        }

    current_hand = found_player.hands[game.current_hand_index]

    return{
        "success": True,
        "hand": current_hand
    }

@app.post("/player/action")
def player_action(request: PlayerAction):
    if game.game_state != GameState.PLAYING:
        return {
            "success": False, 
            "message": "Game is not in playing phase"
        }

    current_player = game.players[game.current_player_index]
    
    if request.player_id != current_player.player_id:
            return {
                "success": False,
                "message": "It's not your turn."
            }
    
    current_hand = current_player.hands[game.current_hand_index]

    # bet_settlement = []

    success, message = game.perform_player_action(
        current_player,
        current_hand,
        request.action
    )

    if success:
        more_turns = game.advance_turn()

    if not more_turns:
        game.play_dealer_turn()
        game.game_state = GameState.ROUND_END
        game.bet_settlements = game.settle_bets()

    return {
        "success": success,
        "message": message,
        "bet_settlements": game.bet_settlements
    }