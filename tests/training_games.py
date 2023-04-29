import random

from game.game import Game
from mab.driver import Driver


def training_games(num_trainings: int, restart: bool = False):
    # Multiplayer game with a random name and three bot players
    print("*** Training Bots ***")
    num_turns = 25
    num_players = 3

    mab_driver = Driver(num_turns, num_players, restart)

    for _ in range(num_trainings):
        name: str = "Training game: " + str(random.randint(0, 10000))
        game = Game(game_name=name, max_players=num_players, num_turns=num_turns)
        game.add_local_player(name='Vuuk', is_observer=False)
        game.add_local_player(name='Egoor', is_observer=False)
        game.add_local_player(name='Ricaardo', is_observer=False)

        game_actions = mab_driver.get_game_actions()
        game.set_game_actions(game_actions)
        game.start()

        winner_index = game.get_winner_index()
        mab_driver.register_winner(winner_index)

        del game
        print()

    mab_driver.pause_training()
