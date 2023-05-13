from src.game import Game

# Run directly from this module, previously having run the remote_test_create as a separate entity
from src.gui.display_manager import DisplayManager


def remote_test_join() -> None:
    # Multiplayer game with a single observer, used to connect to a remote game
    print("*** Remote game test ***")
    name: str = "Test game: Remote Test 691"
    game = Game(game_name=name, max_players=3, num_turns=20, is_full=True)
    game.add_local_player(name="Blue", is_observer=False)
    game.add_local_player(name="Maroon", is_observer=False)

    displayManager = DisplayManager(game, file_name='one_action')
    displayManager.run()

    print()


remote_test_join()
