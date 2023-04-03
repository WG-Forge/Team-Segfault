from src.game import Game


def multiplayer_game():
    # Multiplayer game with three bot players
    print("*** Multiplayer game test ***")
    game = Game(game_name="The test game", num_players=3, num_turns=10)
    game.add_player(name="Jovan", is_bot=True)
    game.add_player(name="Marina", is_bot=False, is_observer=True)
    game.add_player(name="Ricardo", is_bot=True)
    game.add_player(name="Vuk", is_bot=True)
    game.add_player(name="Evgeniy", is_bot=False)
    game.start_game()
    print()
