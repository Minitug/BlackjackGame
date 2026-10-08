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

response = requests.get("http://127.0.0.1:8000/hello")

data = response.json()
print(data["message"])

add_player()

# choice = 'y'

# while True:
#     choice = input("Do you want to add another player? (Y/N)").strip().lower()
#     if choice == 'y':
#         add_player()
#     elif choice == 'n':
#         break
#     else:
#         print("Invalid input.")

# data = response.json()
# print(data["message"])

state = get_game_state(silent = False)
# print(json.dumps(state, indent=4))

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
            # print(json.dumps(state, indent=4))
        else:
            print("Invalid input")
    else:
        # print("Waiting for the host to start the game...")
        time.sleep(1)

state = get_game_state(silent = False)
# print(json.dumps(state, indent=4))
while state["game_state"] == "Betting":
    state = get_game_state(silent = False)
    # print(json.dumps(state, indent=4))
    action_needed_id = ""
    for id in state["players_missing_actions"]:
        if id == player_id:
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

get_game_state(silent = False)