import os
import time
from concurrent.futures import ThreadPoolExecutor

from data.data_io import DataIO
from mab.local_game.local_game import LocalGame
from mab.machine_learining.ml_driver import MLDriver


# Takes about 0.2s per game: 2hrs -> 36 000 games
# If 30 turns per game 5^30 = 9x10^20 combos
# If 5 groups of 6 actions 5^5 = 3125 combos
# Action groups are calculated dynamically based on the number of turns

def train(num_trainings: int = 1, num_turns: int = 15, restart: bool = False) -> None:
    print('*** Training Bots ***')

    mab_driver = MLDriver(num_turns, restart)

    client_map = DataIO.load_client_map()
    game_state = DataIO.load_game_state()

    def train_single_game() -> None:
        game_actions = mab_driver.get_game_actions()
        game: LocalGame
        game = LocalGame(client_map=client_map, game_state=game_state, game_actions=game_actions,
                         num_turns=num_turns)

        winners_index = game.winners_index
        mab_driver.register_winners(winners_index)

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(train_single_game) for _ in range(num_trainings)]
        for future in futures:
            future.result()

    mab_driver.pause_training()


# If you're going to change the number of turns set restart to True for the first training session
for i in range(100):
    start = time.time()
    train(num_trainings=100, num_turns=45, restart=False)
    end = time.time()
    print(f'Time taken {i} (s):', end - start)
