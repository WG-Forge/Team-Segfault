from local_game.local_game import LocalGame
from mab.driver import Driver


def train(num_trainings: int = 1, num_turns: int = 15, num_players: int = 3, restart: bool = False):
    print('*** Training Bots ***')

    mab_driver = Driver(num_turns, num_players, restart)
    for game_num in range(1, num_trainings+1):
        print(f'Game Number: {game_num},', end='')

        game_actions = mab_driver.get_game_actions()
        game = LocalGame(game_actions, num_turns)

        winner_index = game.get_winner_index()
        mab_driver.register_winner(winner_index)

    mab_driver.pause_training()
