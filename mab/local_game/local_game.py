from typing import Dict

from data.data_io import DataIO
from src.game_map.map import Map
from local_game.local_bot import LocalBot


class LocalGame:
    GameActions = dict[int, dict[str, str]]

    def __init__(self, game_actions: GameActions, num_turns: int = 15) -> None:
        self.__winners_index = []
        self.__run(game_actions, num_turns)

    def __run(self, game_actions: GameActions, num_turns: int, num_players=3) -> None:
        current_turn: list[int] = [0]
        current_round: list[int] = [0]

        players: Dict[int, LocalBot] = {
            i: LocalBot(i, game_actions[i], current_turn)
            for i in range(num_players)
        }

        game_map = Map(DataIO.load_client_map(), DataIO.load_game_state(), players,
                       current_turn=current_turn, graphics=False)

        for player in players.values():
            player.add_map(game_map)

        winner, win_type = None, ''
        while not winner and current_turn[0] <= num_turns:
            game_map.register_new_turn()

            player_idx = (current_turn[0] - 1) % num_players
            player = players[player_idx]
            player.register_turn()
            player.run()

            if player.has_capped():
                winner = player
                win_type = 'captured the base'
            current_turn[0] += 1

        max_dp = -1
        player_damages = []
        if not winner:
            for i, player in players.items():
                dp = player.damage_points
                player_damages.append(dp)
                if dp > max_dp:
                    winner = player
                    max_dp = dp
                    win_type = 'most damage'
                elif dp == max_dp:
                    winner = None

        if winner:
            self.__winners_index.append(winner.index)
            print(' Winner is player', self.__winners_index[0], win_type)
        else:
            print(' Draw between players: ', end='')
            for player_index in range(num_players):
                if player_damages[player_index] == max_dp:
                    self.__winners_index.append(player_index)
                    print(player_index, end=', ')
            print()

    @property
    def winners_index(self) -> list[int]: return self.__winners_index
