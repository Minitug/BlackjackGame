class Player:
    def __init__(self, name = "Player", balance = 1000):
        self.name = name
        self.hands = []
        self.balance = balance
        self.starting_balance = balance
        self.winnings = 0
        self.still_playing = True

    def calculate_winnings(self):
        self.winnings = self.balance - self.starting_balance

    def stop_playing(self):
        self.still_playing = False
        self.calculate_winnings
