from game import Game

if __name__ == '__main__':
    game = Game(game_name="The test game", num_players=3, num_turns=45)
    game.add_player(name="Jovan", is_bot=True)
    game.add_player(name="Ricardo", is_bot=True)
    game.add_player(name="Vuk", is_bot=True)
    game.start_game()
    game.join()
