from game.game import Game


def pvp_game(game_name: str, player_name: str, max_players: int = 1, num_turns: int | None = None) -> Game:
    # Maybe have an option of either creating a game or joining an already made one? (with None parameters
    # it will be overridden by the server values,
    # and if the optional parameters don't match when creating a game that already exists a connection will be returned)

    print("called...")
    game = Game(game_name=game_name, max_players=max_players, num_turns=num_turns)

    game.add_local_player(name=player_name, is_observer=False)

    return game
