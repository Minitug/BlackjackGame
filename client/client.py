import requests
import json
import time

player_id = ""
is_host = False

def add_player():
    global player_id, is_host
    name = input("What's your name? ")
    add_player = requests.post(
        "http://127.0.0.1:8000/player/add",
        json={"name": name}
    ).json()
    player_id = add_player["player_id"]
    is_host = add_player["is_host"]
    print(add_player["message"])
    # print(player_id)

def get_game_state(silent = True):
    state = requests.get("http://127.0.0.1:8000/game/state").json()
    if not silent:
        print(json.dumps(state, indent=4))
    return state

def check_if_your_turn(silent = True, expected_game_state = None):
    state = get_game_state(silent = silent)
    while state["game_state"] == expected_game_state:
        for id in state["players_missing_actions"]:
            if id == player_id:
                return True
        # print(f"Gamestate in check_if_your_turn, {expected_game_state}")
        time.sleep(1)
        state = get_game_state(silent = False)
    return False


response = requests.get("http://127.0.0.1:8000/hello")

data = response.json()
print(data["message"])

add_player()

state = get_game_state(silent = False)

while state["game_state"] == "Lobby":
    state = get_game_state()
    if is_host:
        choice = input("Do you want to (S)tart the game or (R)efresh the lobby?").strip().lower()
        print(choice)
        if choice == 's':
            requests.post("http://127.0.0.1:8000/game/start", json={"player_id": player_id})
            break
        elif choice == 'r':
            state = get_game_state(silent = False)
        else:
            print("Invalid input")
    else:
        # print("Gamestate in Lobby")
        time.sleep(1)


your_turn = check_if_your_turn(silent = True, expected_game_state="Betting")
if your_turn:
    new_bet = input("Make your bet: ")
    make_bet = requests.post(
    "http://127.0.0.1:8000/player/bet",
    json={"player_id": player_id,
            "bet_value": new_bet}
    ).json()

    print(make_bet["message"])
    # time.sleep(3)

if state["message"] == "":
    print("Everyone has made their bet")
else:
    print(state["message"])
    print("Someone have not made a bet yet")
time.sleep(1)

state = get_game_state(silent = False)

# print(f"My player id is {player_id}")
# print(f"Gamestate: {state["game_state"]}")

while state["game_state"] == "Playing":
    your_turn = check_if_your_turn(silent = True, expected_game_state = "Playing")
    if your_turn:
        state = get_game_state(silent=True)
        options = state["options"]
        valid_choices = state["valid_choices"]
        
        get_hand = requests.get(
        f"http://127.0.0.1:8000/player/{player_id}/hand"
        ).json()

        cards = get_hand["hand"]["cards"]

        formatted_cards = ", ".join(
            f"{card['rank']} of {card['suit']}"
            for card in cards
        )

        hand_value = get_hand["hand"]["value"]

        print(f"Hand consists of: {formatted_cards}. Value of cards: {hand_value}")

        # print(f"Hand consists of {get_hand["message"]["cards"]}")
        
        choice_text = f"Do you want to {', '.join(options)}? ({'/'.join(valid_choices)}): "
        get_action = input(choice_text).strip().upper()

        make_action = requests.post(
            "http://127.0.0.1:8000/player/action",
            json={"player_id": player_id,
                  "action": get_action}
        ).json()
        print(make_action["message"])

    time.sleep(1)
    # print("Gamestate in Playing")
    state = get_game_state()

state = get_game_state(silent=False)

for settlement in make_action["bet_settlements"]:
    print(settlement)