import random

from game.game import Game


def multiplayer_game(game_name: str, *player_names) -> Game:
    # Multiplayer game with a random name and three bot players
    print("*** Multiplayer game test ***")
    name: str = game_name
    name += str(random.randint(0, 10000))
    game = Game(game_name=name, max_players=3, num_turns=45)
    # displayManager = DisplayManager(game)

    for player_name in player_names:
        game.add_local_player(name=player_name, is_observer=False)

    # displayManager.run()

    print()
    return game
