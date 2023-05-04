from src.game import Game


def single_player_game(game_name: str, player_name: str) -> Game:
    game = Game(game_name=game_name, max_players=1, num_turns=15)
    game.add_local_player(name=player_name, is_observer=False)

    return game
