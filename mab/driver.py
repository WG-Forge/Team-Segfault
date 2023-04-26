import json
from typing import Dict, List, Type, cast

from mab.player import Player


class Driver:
    __results_table_path = "mab\\training_data\\results_table.json"
    __num_games_path = "mab\\training_data\\num_games.json"
    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.03  # Minimum exploration probability -> 3 %
    __decay_per_game = 0.0001  # Minimum exploration ratio reached after about 10 000 games

    # GameActions = {player_index: {tank_name: action_combo}}
    GameActions = Type[Dict[int, Dict[str, str]]]
    # ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
    ResultsTable = Type[Dict[int, Dict[str, Dict[str, List[int]]]]]

    def __init__(self, num_turns: int, num_players: int, restart=False):
        # Player index corresponds to who starts first, so Players[0] plays turn 1
        self.__players = {agent_index: Player(num_turns) for agent_index in range(num_players)}
        self.__explore_prob: float = 1.0
        if not restart:
            self.__continue_training()

    def get_game_actions(self) -> GameActions:
        game_actions = {}
        for player_index, player in self.__players.values():
            game_actions[player_index] = player.get_game_actions(self.__explore_prob)
        return cast(Driver.GameActions, game_actions)

    def register_winner(self, winner_index: int) -> None:
        for player_index, player in self.__players.items():
            if player_index == winner_index:
                player.register_reward(1)
            else:
                player.register_reward(0)
        self.__update_exploring()

    def __update_exploring(self) -> None:
        if self.__explore_prob > Driver.__min_explore_prob:
            self.__explore_prob -= Driver.__decay_per_game

    def __continue_training(self) -> None:
        results_table = Driver.load_results_table_from_json()
        for index, player in self.__players.items():
            player.set_results_table(results_table[index])

        num_games = Driver.load_num_games_from_json()
        self.__explore_prob = Driver.calc_explore_prob(num_games)

    def pause_training(self) -> None:
        results_table = {index: player.get_results_table() for index, player in self.__players.items()}
        Driver.dump_results_table_to_json(cast(Driver.ResultsTable, results_table))
        Driver.dump_num_games_to_json(self.__explore_prob)

    @staticmethod
    def calc_explore_prob(num_games: int) -> float:
        total_decay = Driver.__decay_per_game * num_games
        return float(1 - total_decay)

    @staticmethod
    def dump_results_table_to_json(results_table: ResultsTable) -> None:
        # results_table = {player_index: {tank_name: {action_combo: [rewards list]}}}
        with open(Driver.__results_table_path, 'w') as file:
            json.dump(results_table, file)

    @staticmethod
    def dump_num_games_to_json(explore_prob) -> None:
        num_games = int((Driver.__max_explore_prob - explore_prob) / Driver.__decay_per_game)
        with open(Driver.__num_games_path, 'w') as file:
            json.dump(num_games, file)

    @staticmethod
    def load_results_table_from_json() -> ResultsTable:
        with open(Driver.__results_table_path, 'r') as file:
            results_table = json.load(file)
        return results_table

    @staticmethod
    def load_num_games_from_json() -> int:
        with open(Driver.__num_games_path, 'r') as file:
            num_games = json.load(file)
        return num_games
