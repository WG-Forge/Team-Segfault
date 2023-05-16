import random as rnd
import statistics

from mab.machine_learning.ml_tank import MLTank


class MLPlayer:
    __tank_shorts = ('s', 'l', 'h', 'm', 'a')

    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.25  # Minimum exploration probability -> 3 %
    __decay_per_game = 0.0000375  # Minimum exploration ratio reached after about 20 000 games

    def __init__(self, num_rounds: int, group_size: int):
        self.__tanks: dict[str, MLTank] = self.__make_tanks(num_rounds, group_size)
        self.__explore_prob: float = self.__max_explore_prob
        self.__results: dict[str, list[int]] = {}
        self.__game_tank_action_combos: str = ''  # String representing actions taken this game

    def update_exploring(self) -> None:
        if self.__explore_prob > self.__min_explore_prob:
            self.__explore_prob -= self.__decay_per_game

    def __make_tanks(self, num_rounds: int, group_size: int) -> dict[str, MLTank]:
        return {
            name: MLTank(num_rounds, group_size)
            for name in self.__tank_shorts
        }

    def register_reward(self, reward: int) -> None:
        # If the combination of arms used in this turn has never been used create a new entry in
        # results with a string that represents the combination of tank-actions as the key and a list of
        # the rewards associated with this combo. Append this reward to this list.
        action_rewards = self.__results.setdefault(self.__game_tank_action_combos, [])
        action_rewards.append(reward)

        # If the list of rewards associated with this arm has many items, remove the first item
        # such that results when the enemies have not been trained are not taken into account
        if len(action_rewards) > 30:
            action_rewards.pop(0)

    def get_explore_actions(self) -> str:
        tank_action_combos = [name + tank.get_explore_actions() for name, tank in self.__tanks.items()]
        self.__game_tank_action_combos = ''.join(tank_action_combos)
        return self.__game_tank_action_combos

    def get_exploit_actions(self) -> str:
        # Returns a string representing the combination of tank-arms with the highest average reward so far
        averages = {
            tank_arm_combo: statistics.mean(rewards) if rewards else 0
            for tank_arm_combo, rewards in self.__results.items()
        }
        return max(averages, key=averages.get)

    def get_game_actions(self) -> str:
        return self.get_explore_actions() if rnd.random() < self.__explore_prob else self.get_exploit_actions()

    def set_explore_prob(self, num_games: int) -> None:
        self.__explore_prob = self.__calc_explore_prob(num_games)

    @property
    def results_table(self) -> dict[str, list[int]]: return self.__results

    @results_table.setter
    def results_table(self, results_table: dict[str, list[int]]) -> None: self.__results = results_table

    @staticmethod
    def __calc_explore_prob(num_games: int) -> float:
        total_decay = MLPlayer.__decay_per_game * num_games
        return float(1 - total_decay)
