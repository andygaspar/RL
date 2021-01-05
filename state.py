

class State:

    def __init__(self, dealer: int, player:int, terminal: bool = False):
        self.dealer = dealer
        self.player = player
        self.terminal = terminal

    def __repr__(self):
        return str([self.dealer, self.player, self.terminal])