from game import Game

if __name__ == '__main__':
    game = Game()
    game.add_player(name="Ricardo", is_bot=False)
    game.start_game()
    game.join()
