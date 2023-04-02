from game import Game

if __name__ == '__main__':
    game = Game()
    game.add_player(name="playa", is_bot=True)
    game.start_game()
    game.join()
