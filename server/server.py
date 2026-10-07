import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from blackjack.players import Player
from blackjack.game import BlackjackGame, GameState

class PlayerRequest(BaseModel):
    name: str

class StartGameRequest(BaseModel):
    player_id: str

class PlayerBet(BaseModel):
    player_id: str
    bet_value: int


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
    "Welcome to Blackjack!\n"
    "You start with a balance of $1000.\n"
    "You win by leaving the table with more money than you started with.\n"
    # "Do you want to play against a (D)ealer (up to 5 players) or 1v1 in (P)vP? (D/P)"
    )
    return{"message": message}


@app.post("/game/start")
def start_game(request: StartGameRequest):
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
    waiting_players_to_bet_ids = []

    if game.game_state == GameState.BETTING:
        all_players_bet = all(
            player.hands[0].bet is not None
            for player in game.players
        )


        if not all_players_bet:
            for player in game.players:
                if player.hands[0].bet == None:
                    waiting_players_to_bet.append(player.name)
                    waiting_players_to_bet_ids.append(player.player_id)
            message = "Waiting for players: " + ", ".join(waiting_players_to_bet) + "."

        else:
            game.game_state = GameState.PLAYING #Change later! get_game_state should NOT change it

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
        "message": message,
        "players_missing_actions": waiting_players_to_bet_ids
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
    for player in game.players:
        if player.player_id == request.player_id:
            found_player = player
            break

    if found_player == None:
        return {"message": "Player was not found"}

    found_player.hands[0].bet = request.bet_value