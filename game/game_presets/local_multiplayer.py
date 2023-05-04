from game.game import Game


def local_multiplayer_game(game_name: str, *player_names: str, max_players: int = 3, num_turns: int = 45) -> Game:
    game = Game(game_name=game_name, max_players=max_players, num_turns=num_turns)

    for player_name in player_names:
        game.add_local_player(name=player_name, is_observer=False)

    return game
