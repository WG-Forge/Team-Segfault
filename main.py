from src.gui.display_manager import DisplayManager
from mab.train import train

if __name__ == '__main__':
    display_manager = DisplayManager()
    display_manager.run()

    # train(num_trainings=10, num_turns=45, restart=False)
