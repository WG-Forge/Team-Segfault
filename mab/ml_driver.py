from typing import Type, cast

from data.data_io import DataIO
from mab.ml_player import MLPlayer


class MLDriver:
    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.03  # Minimum exploration probability -> 3 %
    __decay_per_game = 0.0001  # Minimum exploration ratio reached after about 10 000 games

    # GameActions = {player_index: {tank_name: action_combo}}
    GameActions = Type[dict[int, dict[str, str]]]
    # ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
    ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]

    def __init__(self, num_turns: int, restart=False, num_players: int = 3):
        # Player index corresponds to who starts first, so Players[0] plays turn 1
        group_size = self.calc_action_group_size(num_turns)
        self.__players = {agent_index: MLPlayer(num_turns, group_size) for agent_index in range(num_players)}
        self.__explore_prob: float = 1.0
        if not restart:
            self.__continue_training()

    def get_game_actions(self) -> GameActions:
        game_actions = {}
        for player_index, player in self.__players.items():
            game_actions[player_index] = player.get_game_actions(self.__explore_prob)
        return cast(self.GameActions, game_actions)

    def register_winner(self, winner_index: int) -> None:
        for player_index, player in self.__players.items():
            if player_index == winner_index:
                player.register_reward(1)
            else:
                player.register_reward(0)
        self.__update_exploring()

    def __update_exploring(self) -> None:
        if self.__explore_prob > self.__min_explore_prob:
            self.__explore_prob -= self.__decay_per_game

    def __continue_training(self) -> None:
        results_table = DataIO.load_results_table()
        for index, player in self.__players.items():
            player.set_results_table(results_table[str(index)])

        num_games = DataIO.load_num_games()
        self.__explore_prob = self.calc_explore_prob(num_games)

    def pause_training(self) -> None:
        results_table = {index: player.get_results_table() for index, player in self.__players.items()}
        DataIO.save_results_table(cast(self.ResultsTable, results_table))
        DataIO.save_num_games(self.__explore_prob, self.__max_explore_prob, self.__decay_per_game)

    @staticmethod
    def calc_action_group_size(num_turns: int, action_num: int = 5, max_combos: int = 10000) -> int:
        size = 1
        while action_num ** (num_turns / size) > max_combos:
            size += 1
        return size - 1

    @staticmethod
    def calc_explore_prob(num_games: int) -> float:
        total_decay = MLDriver.__decay_per_game * num_games
        return float(1 - total_decay)
