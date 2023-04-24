import random

from game.game import Game


def multiplayer_game():
    # Multiplayer game with a random name and three bot players
    print("*** Multiplayer game test ***")
    name: str = "Test game: "
    name += str(random.randint(0, 10000))
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.add_local_player(name="Vuuk", is_observer=False)
    game.add_local_player(name="Egoor", is_observer=True)
    game.add_local_player(name="Ricaardo", is_observer=False)
    game.add_local_player(name="Jovaan", is_observer=True)
    game.add_local_player(name="Igoor", is_observer=False)
    game.add_local_player(name="Dariijush", is_observer=False)
    game.start_menu()
    print()
