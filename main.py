from tests.multiplayer_game import multiplayer_game
from tests.training_games import training_games
from tests.training_locally import train
import time

if __name__ == '__main__':
    # multiplayer_game()
    # training_games(num_trainings=1, restart=True)

    # If you're going to change the number of turns set restart to True for the first training session
    start = time.time()
    train(num_trainings=10, num_turns=30, restart=False)
    end = time.time()


    print('Time taken (s):', end-start)
