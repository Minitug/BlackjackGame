import requests
import json

def add_player():
    name = input("What's your name? ")
    requests.post(
        "http://127.0.0.1:8000/player/add",
        json={"name": name}
)

def get_game_state():
    state = requests.get("http://127.0.0.1:8000/game/state").json()
    print(json.dumps(state, indent=4))

response = requests.get("http://127.0.0.1:8000/hello")

data = response.json()
print(data["message"])

add_player()

# choice = 'y'

while True:
    choice = input("Do you want to add another player? (Y/N)").strip().lower()
    if choice == 'y':
        add_player()
    elif choice == 'n':
        break
    else:
        print("Invalid input.")

data = response.json()
print(data["message"])

requests.post("http://127.0.0.1:8000/game/start")

get_game_state()



