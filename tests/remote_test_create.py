from game.game import Game


def remote_test_create():
    # Multiplayer game with a fixed name and three bot players
    print("*** Remote joining game test ***")
    name: str = "Test game: Remote7"
    game = Game(game_name=name, max_players=3, num_turns=45)
    game.add_local_player(name="Vuk", is_observer=False)
    game.add_local_player(name="Egor", is_observer=False)
    game.add_local_player(name="Ricardo", is_observer=False)
    game.start_menu()
    print()


remote_test_create()
