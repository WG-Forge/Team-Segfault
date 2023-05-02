from game.game import Game
from gui.display_manager import DisplayManager


def single_player_game() -> None:
    # Single-player game with one bot player
    print("*** Single-player game test ***")
    game = Game(game_name="Test single player", max_players=1, num_turns=15)
    game.add_local_player(name="The guy", is_observer=False)

    displayManager = DisplayManager(game)
    displayManager.run()

    print()


single_player_game()
