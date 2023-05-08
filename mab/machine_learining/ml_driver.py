from typing import Type, cast

from data.data_io import DataIO
from mab.machine_learining.ml_player import MLPlayer


class MLDriver:
    # GameActions = {player_index: {tank_name: action_combo}}
    GameActions = Type[dict[int, dict[str, str]]]
    # ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
    ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]

    def __init__(self, num_turns: int, restart=False, num_players: int = 3):
        # Player index corresponds to who starts first, so Players[0] plays turn 1
        group_size = self.calc_action_group_size(num_turns)
        print('group_size', group_size)
        self.__players = {
            agent_index: MLPlayer(num_turns, group_size)
            for agent_index in range(num_players)
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
        self.__game_num = DataIO.load_num_games()
        results_table = DataIO.load_results_table()
        for index, player in self.__players.items():
            player.set_results_table(results_table[str(index)])
            player.set_explore_prob(self.__game_num)

    def pause_training(self) -> None:
        results_table = {index: player.get_results_table() for index, player in self.__players.items()}
        DataIO.save_results_table(cast(self.ResultsTable, results_table))
        DataIO.save_num_games(self.__game_num)
        DataIO.save_best_actions(self.__get_exploit_actions())

    @staticmethod
    def calc_action_group_size(num_turns: int, action_num: int = 5, max_combos: int = 10000) -> int:
        size = 1
        while action_num ** (num_turns / size) > max_combos:
            size += 1
        return size - 1
