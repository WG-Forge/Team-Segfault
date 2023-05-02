from game.game import Game


def spectator_game(game_name: str, player_name: str) -> Game:
    # the other parameters like num_players and num_turns will be filled in from the server

    game = Game(game_name=game_name)
    game.add_local_player(name=player_name, is_observer=True)

    return game
