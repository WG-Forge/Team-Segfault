from src.game import Game

# Run directly from this module, and then run the remote_test_join as a separate entity
from src.gui.display_manager import DisplayManager


def remote_test_create() -> None:
    # Multiplayer game with a fixed player_name and three bot players
    print("*** Remote game test ***")
    name: str = "Test game: Remote Test 645"
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.add_local_player(name="Hazel", is_observer=False)
    game.add_local_player(name="Violet", is_observer=True)
    game.add_local_player(name="Green", is_observer=True)

    displayManager = DisplayManager(game)
    displayManager.run()

    print()


remote_test_create()
