from game.game import Game


def remote_test_join():
    # Multiplayer game with a single observer, used to connect to a remote game
    name: str = "Test game: Remote7"
    game = Game(game_name=name)
    game.add_local_player(name="John Doe", is_observer=True)
    game.start_menu()


remote_test_join()
