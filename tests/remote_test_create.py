from game.game import Game


# Run directly from this module, and then run the remote_test_join as a separate entity

def remote_test_create():
    # Multiplayer game with a fixed name and three bot players
    print("*** Remote game test ***")
    name: str = "Test game: Remote Test 100"
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.add_local_player(name="Blue", is_observer=False)
    game.add_local_player(name="Pink", is_observer=False)
    game.add_local_player(name="Orange", is_observer=True)
    game.add_local_player(name="Green", is_observer=True)
    game.start_menu()
    print()


remote_test_create()
