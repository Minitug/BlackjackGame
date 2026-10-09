# Blackjack Game

A multiplayer Blackjack game developed in Python and C# as part of a programming project.

Python handles the core Blackjack logic and runs a FastAPI server that manages players, game state, betting, and actions. Players can connect using either a Python terminal client or a C# Windows Forms GUI.

## Features

### Blackjack Gameplay

- Standard 52-card deck with shuffling and drawing
- Hand value calculation, including Ace handling
- Hit and Stand
- Bust and Blackjack detection
- Player balances and betting
- Double Down, Split, and Surrender
- Dealer gameplay
- Multiple rounds and bet settlements

### Multiplayer

- Multiple players can join the same game
- The first player to join becomes the host
- The host starts the game
- Players place bets and take actions through the server
- The terminal client and Windows Forms GUI can participate in the same game

### Windows Forms GUI

- Join screen and automatically updating multiplayer lobby
- Host-controlled game start
- Betting interface with balance validation
- Player hand and dealer hand displays
- Hit, Stand, Double, Split, and Surrender buttons
- Unavailable actions disabled and greyed out
- Automatic balance and game-status updates
- Round results showing players' hands, the dealer's hand, and settlements
- Previous round results remain visible during subsequent rounds

The GUI polls the server approximately once per second to stay synchronized.

## Technologies

- **Python:** Blackjack logic and terminal client
- **FastAPI:** REST API and multiplayer game management
- **Uvicorn:** Python web server
- **C# / .NET 10:** Windows Forms GUI
- **HTTP / JSON:** Client-server communication

## Project Structure

```text
blackjack_game/
├── .gitignore
├── README.md
├── main.py
├── blackjack/
│   ├── __init__.py
│   ├── cards.py
│   ├── game.py
│   └── players.py
├── server/
│   └── server.py
├── client/
│   └── client.py
├── BlackjackGUI/
│   ├── BlackjackGUI.slnx
│   ├── BlackjackGUI.csproj
│   ├── Program.cs
│   ├── BlackjackForm.cs
│   ├── BlackjackForm.Designer.cs
│   ├── BlackjackForm.resx
│   ├── GameStateResponse.cs
│   └── JoinResponse.cs
└── tests/
    └── test_cards.py
```

Generated folders such as `__pycache__`, `.pytest_cache`, `bin`, and `obj` are omitted.

## Running the Game

### Requirements

- Python and the project's Python dependencies, including FastAPI and Uvicorn
- Windows with .NET 10 for the Windows Forms GUI
- Visual Studio with the **.NET desktop development** workload to build and run the GUI from source

### 1. Start the Python server

From the repository root, run:

```powershell
py -m uvicorn server.server:app --reload
```

The server runs at `http://127.0.0.1:8000` by default. FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

Keep the server running while using a client.

### 2. Start the Windows Forms GUI

1. Open `BlackjackGUI/BlackjackGUI.slnx` in Visual Studio.
2. Build and run the project.
3. Enter a player name and click **Join**.
4. If you are the host, click **Start Game** when ready.
5. Place a bet and play Blackjack.

You can open multiple GUI instances to test multiplayer locally.

### 3. Start the Python terminal client (alternative)

With the server running, open another terminal in the repository root and run:

```powershell
py -m client.client
```

### Playing a round

1. Players join the game.
2. The host starts the game.
3. Players place their bets.
4. Players perform Blackjack actions when permitted.
5. The server resolves the round, calculates settlements, and updates balances.
6. Players can review the results and continue into subsequent rounds.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/player/add` | Join the game |
| GET | `/game/state` | Retrieve the current game state |
| POST | `/game/start` | Start the game as host |
| POST | `/player/bet` | Submit a bet |
| POST | `/player/action` | Perform a Blackjack action |
| GET | `/player/{player_id}/hand/{hand_index}` | Retrieve a player's hand |

The server validates actions, controls game progression, and calculates results.

## Testing

The repository contains automated card tests in `tests/test_cards.py`. From the repository root, run:

```powershell
py -m pytest
```

## Notes

- Start the Python server before launching a client.
- The GUI is a Windows application.
- The clients currently connect to the local server at `127.0.0.1:8000`.
- The GUI uses periodic HTTP polling rather than WebSockets.
