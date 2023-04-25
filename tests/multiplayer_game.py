import random

from game.game import Game


def multiplayer_game():
    # Multiplayer game with a random name and three bot players
    print("*** Multiplayer game test ***")
    name: str = "Test game 2: "
    name += str(random.randint(0, 10000))
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.load_game_info([('This will be overwritten', False), ("Vuk", False), ("Ricardo", False), ("Jovan", True)])
    game.start_menu()
    print()
