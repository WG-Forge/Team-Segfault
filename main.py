from src.gui.display_manager import DisplayManager
# from tests.multiplayer_game import multiplayer_game
from mab.train import train
from mab.data.results_eval import results_eval


if __name__ == '__main__':
    # display_manager = DisplayManager()
    # display_manager.run()

    # multiplayer_game()

    results_eval()

    # train(num_trainings=25_000,
    #       num_rounds=15,
    #       restart=False,
    #       num_players=3,
    #       num_actions=1,
    #       save_file='many_actions')
