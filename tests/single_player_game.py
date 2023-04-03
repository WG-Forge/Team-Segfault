from src.game import Game


def single_player_game():
    # Single-player game with one bot player
    print("*** Single-player game test ***")
    game = Game()
    game.add_player(name="The guy", is_bot=True)
    game.start_game()
    print()
