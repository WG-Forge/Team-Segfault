from game import Game


# Run directly from this module, previously having run the remote_test_create as a separate entity

def remote_test_join():
    # Multiplayer game with a single observer, used to connect to a remote game
    print("*** Remote game test ***")
    name: str = "Test game: Remote Test 100"
    game = Game(game_name=name)
    game.add_local_player(name="Reed", is_observer=True)
    game.start_menu()
    print()


remote_test_join()
