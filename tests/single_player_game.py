from game.game import Game


def single_player_game():
    # Single-player game with one bot player
    print("*** Single-player game test ***")
    game = Game()
    game.add_local_player(name="The guy", is_observer=False)
    game.start_game()
    print()
