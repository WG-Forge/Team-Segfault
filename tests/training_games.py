import random

from game.game import Game
from cmab.driver import Driver


def training_games(num_trainings: int, restart: bool = False):
    # Multiplayer game with a random name and three bot players
    print("*** Training Bots ***")
    num_turns = 15
    player_names = ("Player1", "Player2", "Player3")

    cmab_driver = Driver(num_turns, player_names, restart)

    for _ in range(num_trainings):
        name: str = "Training game: " + str(random.randint(0, 10000))
        game = Game(game_name=name, max_players=3, num_turns=15, graphics=True)
        game.add_player(name=player_names[0], is_bot=True, is_observer=False)
        game.add_player(name=player_names[1], is_bot=True, is_observer=False)
        game.add_player(name=player_names[2], is_bot=True, is_observer=False)

        game_actions = cmab_driver.get_game_actions()
        game.start_game(game_actions)
        winner_name = game.get_winner_name()
        cmab_driver.register_game_results(winner_name, game_actions)
        cmab_driver.pause_training()

        del game
        print()
