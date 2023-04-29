import random

from game.game import Game
from gui.display_manager import DisplayManager


def multiplayer_game():
    # Multiplayer game with a random name and three bot players
    print("*** Multiplayer game test ***")
    name: str = "Test game 1: "
    name += str(random.randint(0, 10000))
    game = Game(game_name=name, max_players=3, num_turns=45)
    displayManager = DisplayManager(game)

    game.add_local_player(name="Vuk", is_observer=False)
    game.add_local_player(name="Egor", is_observer=True)
    game.add_local_player(name="Ricardo", is_observer=False)
    game.add_local_player(name="Jovan", is_observer=True)
    game.add_local_player(name="Igor", is_observer=False)
    game.add_local_player(name="John Doe", is_observer=False)

    displayManager.run()

    print()
