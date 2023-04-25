import random

from constants import PLAYER1_NAME
from game.game import Game


def multiplayer_game():
    # Multiplayer game with a random name and three bot players
    print("*** Multiplayer game test ***")
    name: str = "Test game 2: "
    name += str(random.randint(0, 10000))
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.add_local_player(name=PLAYER1_NAME, is_observer=False)
    game.add_local_player(name="Egor1", is_observer=True)
    game.add_local_player(name="Ricardo1", is_observer=False)
    game.add_local_player(name="Jovan1", is_observer=True)
    game.add_local_player(name="Igor1", is_observer=False)
    game.add_local_player(name="Darijush1", is_observer=False)
    game.start_menu()
    print()
