from mab.local_game.local_game import LocalGame
from mab.machine_learning.ml_driver import MLDriver


# Takes about 0.2s per game: 2hrs -> 36 000 games
# If 30 turns per game 5^30 = 9x10^20 combos
# If 5 groups of 6 actions 5^5 = 3125 combos
# Action groups are calculated dynamically based on the number of turns

def train(num_trainings: int = 1,
          num_rounds: int = 15,
          restart: bool = False,
          num_players: int = 3,
          num_actions: int = 1,
          save_file: str = 'default') -> None:

    num_turns = num_rounds * num_players

    print('*** Training Bots ***')

    mab_driver = MLDriver(num_rounds, restart, num_players, num_actions, save_file)

    for game_num in range(1, num_trainings + 1):
        print(f'Game Number: {game_num},', end='')

        game_actions = mab_driver.get_game_actions()
        game = LocalGame(game_actions, num_turns)

        winners_index = game.winners_index
        mab_driver.register_winners(winners_index)

    mab_driver.pause_training()

# If you're going to change the number of turns set restart to True for the first training session
# start = time.time()
# train(num_trainings=10, num_turns=30, restart=False)
# end = time.time()

# print('Time taken (s):', end-start)
