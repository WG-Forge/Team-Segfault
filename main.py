# from tests.single_player_game import single_player_game
from tests.multiplayer_game import multiplayer_game
from time_test import time_test

if __name__ == '__main__':
    # todo: add finish screen
    # single_player_game()
    time_test(multiplayer_game)
