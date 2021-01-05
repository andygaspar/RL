import dock
from state import State


def step(state: State, action):

    if action == "hit":
        player = state.player + dock.pick()

        if player > 21 or player < 1:
            return State(state.dealer, player, True), - 1

        else:
            return State(state.dealer, player, False), 0

    dealer = state.dealer

    while True:
        dealer += dock.pick()

        if dealer > 21 or dealer < 1:
            return State(dealer, state.player, True), 1

        if 17 <= dealer:
            if dealer > state.player:
                return State(dealer, state.player, True), -1
            if dealer == state.player:
                return State(dealer, state.player, True), 0
            else:
                return State(dealer, state.player, True), 1


