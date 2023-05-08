import random

from src.constants import DEFAULT_NUM_TURNS
from src.constants import PLAYER_NAMES
from src.game import Game


def local_game(num_players: int = 3, num_turns: int = DEFAULT_NUM_TURNS, is_full: bool = False) -> Game:
    game_name: str = ''
    if num_players > 1:
        game_name = 'Test game ' + str(random.randint(0, 10000))
    if num_turns < 1:
        num_turns = DEFAULT_NUM_TURNS

    game = Game(game_name=game_name, max_players=num_players, num_turns=num_turns, is_full=is_full)

    for i in range(num_players):
        game.add_local_player(name=PLAYER_NAMES[i + 1], is_observer=False)

    return game
