class Player:
    def __init__(self, name = "Player", balance = 1000, player_id = ""):
        self.name = name
        self.hands = []
        self.balance = balance
        self.starting_balance = balance
        self.winnings = 0
        self.still_playing = True
        self.player_id = player_id

    def calculate_winnings(self):
        self.winnings = self.balance - self.starting_balance

    def stop_playing(self):
        self.still_playing = False
        self.calculate_winnings()
