import time
import json
import requests

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

def format_cards(cards):
    return ", ".join(
                f"{card['rank']} of {card['suit']}"
                for card in cards
            )

def check_if_your_turn(silent = True, expected_game_state = None):
    state = get_game_state()
    me = next(
            (player for player in state["players"]
             if player["player_id"] == player_id),
            None
        )

    if me is not None and not me["still_playing"]:
        return False

    if player_id in state["players_missing_actions"]:
        return True

    time.sleep(1)
    state = get_game_state()

    return False

def handle_betting():
    state = get_game_state()
    your_turn = check_if_your_turn(expected_game_state="Betting")
    if your_turn:
        state = get_game_state()
        if state["game_state"] != "Betting":
            return True
        
        new_bet = input("Make your bet: ")
        make_bet = requests.post(
        "http://127.0.0.1:8000/player/bet",
        json={"player_id": player_id,
                "bet_value": new_bet}
        ).json()

        state = get_game_state()

        print(make_bet["message"])

        if make_bet.get("left_table"):
            return False

    if state["game_state"] == "Betting":
        if state["message"]:
            print(state["message"])

    elif state["game_state"] == "Playing":
        print("Everyone has made their bet")
        # print("Someone have not made a bet yet")
    time.sleep(1)
    return True

def handle_playing():
    state = get_game_state()
    while state["game_state"] == "Playing":
        your_turn = check_if_your_turn(expected_game_state = "Playing")
        if your_turn:
            state = get_game_state()

            options = state["options"]
            valid_choices = state["valid_choices"]

            hand_index = state["current_hand_index"]

            get_hand = requests.get(
                f"http://127.0.0.1:8000/player/{player_id}/hand/{hand_index}"
            ).json()

            cards = get_hand["hand"]["cards"]

            formatted_cards = format_cards(cards)

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

            if make_action["success"]:
                hand_response = requests.get(
                    f"http://127.0.0.1:8000/player/{player_id}/hand/{hand_index}"
                ).json()
                
                hand = hand_response["hand"]

                print(f"Hand: {format_cards(hand['cards'])}")
                print(f"Value: {hand['value']}")

                if hand["bust"]:
                    print("BUST! Your turn is over.")
                elif hand["stand"]:
                    print("You stand. Your turn is over.")
                elif hand["double_down"]:
                    print("Double down complete. Your turn is over.")
                elif hand["surrender"]:
                    print("You surrendered. Your turn is over.")

        time.sleep(1)
        # print("Gamestate in Playing")
        state = get_game_state()

def show_settlements():
    state = get_game_state()

    print("\n========== ROUND RESULTS ==========\n")

    for player in state["players"]:
        print(f"{player['name']}'s hand:")

        for hand in player["hands"]:
            print(f"  {format_cards(hand['cards'])}")
            print(f"  Value: {hand['value']}")

    dealer = state["dealer_hand"]

    print("\nDealer's hand:")
    print(f"  {format_cards(dealer['cards'])}")
    print(f"  Value: {dealer['value']}")

    print("\n------------- RESULTS -------------\n")


    for settlement in state["bet_settlements"]:
        print(settlement)

response = requests.get("http://127.0.0.1:8000/hello")

data = response.json()
print(data["message"])

add_player()

state = get_game_state()

while state["game_state"] == "Lobby":
    state = get_game_state()
    if is_host:
        choice = input("Do you want to (S)tart the game or (R)efresh the lobby?").strip().lower()
        print(choice)
        if choice == 's':
            requests.post("http://127.0.0.1:8000/game/start", json={"player_id": player_id})
            break
        elif choice == 'r':
            state = get_game_state()
        else:
            print("Invalid input")
    else:
        # print("Gamestate in Lobby")
        time.sleep(1)

settlements_shown = False

while True:
    state = get_game_state()

    if state["game_state"] == "Betting":
        settlements_shown = False

    if handle_betting() is False:
        state = get_game_state()

    elif state["game_state"] == "Playing":
        handle_playing()

    elif state["game_state"] == "Round End":
        if not settlements_shown:
            show_settlements()
            settlements_shown = True


    me = next(
        (player for player in state["players"]
        if player["player_id"] == player_id),
        None
    )

    if me is not None and not me["still_playing"]:
        winnings = me["winnings"]

        print("\nYou have left the table.")

        if winnings > 0:
            print(f"You won ${winnings:.2f}!")
        elif winnings < 0:
            print(f"You lost ${-winnings:.2f}.")
        else:
            print("You broke even.")

        print("Thank you for playing!")
        break

    time.sleep(1)


