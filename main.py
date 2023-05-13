from src.gui.display_manager import DisplayManager
from mab.train import train

if __name__ == '__main__':
    display_manager = DisplayManager(file_name='one_action')
    display_manager.run()

    # train(num_trainings=10000,
    #       num_rounds=15,
    #       restart=False,
    #       num_players=3,
    #       num_actions=1,
    #       save_file='one_action')
