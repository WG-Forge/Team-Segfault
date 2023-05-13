from math import ceil
from typing import Type, cast

from data.data_io import DataIO
from mab.machine_learining.ml_player import MLPlayer


class MLDriver:
    # GameActions = {player_index: {tank_name: action_combo}}
    GameActions = Type[dict[int, dict[str, str]]]
    # ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
    ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]

    def __init__(self, num_rounds: int = 15,
                 restart: bool = False,
                 num_players: int = 3,
                 num_actions: int = 1,
                 save_file: str = 'default'):

        self.__save_file = save_file
        group_size = ceil(num_rounds/num_actions)

        self.__players = {  # Player index corresponds to who starts first, so Players[0] plays turn 1
            player_index: MLPlayer(num_rounds, group_size)
            for player_index in range(num_players)
        }

        self.__game_num: int = 0
        if not restart:
            self.__continue_training()

    def __get_exploit_actions(self) -> GameActions:
        return cast(self.GameActions, {
            player_index: player.get_exploit_actions()
            for player_index, player in self.__players.items()
        })

    def get_game_actions(self) -> GameActions:
        return cast(self.GameActions, {
            player_index: player.get_game_actions()
            for player_index, player in self.__players.items()
        })

    def register_winners(self, winners_index: list[int]) -> None:
        for player_index, player in self.__players.items():
            if player_index in winners_index:
                player.register_reward(1)
            else:
                player.register_reward(0)
            player.update_exploring()
        self.__game_num += 1

    def __continue_training(self) -> None:
        self.__game_num = DataIO.load_num_games(self.__save_file)
        results_table = DataIO.load_results_table(self.__save_file)
        for index, player in self.__players.items():
            player.set_results_table(results_table[str(index)])
            player.set_explore_prob(self.__game_num)

    def pause_training(self) -> None:
        results_table = {
            index: player.get_results_table()
            for index, player in self.__players.items()
        }

        DataIO.save_session_data(results_table, self.__game_num, self.__get_exploit_actions(), self.__save_file)
