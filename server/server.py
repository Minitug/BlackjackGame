from fastapi import FastAPI
from blackjack.game import BlackjackGame

app = FastAPI()

@app.get("/hello")
def hello():
    message = (
    "Welcome to Blackjack!\n"
    "You start with a balance of $1000.\n"
    "You win by leaving the table with more money than you started with.\n"
    "Do you want to play against a (D)ealer (up to 5 players) or 1v1 in (P)vP? (D/P)"
    )
    return{"message": message}


@app.post("/game/start")
def start_game():
    global game

    game = BlackjackGame()

    return {
        "message": "Game created",
        "minimum_bet": game.minimum_bet
    }


@app.get("/game/state")
def get_game_state():
    if game is None:
        return{"error": "No game has been started"}

    return {
        "minimum_bet": game.minimum_bet,
        "cards_remaining": game.deck.cards_remaining()
    }