import json
import random as rnd
from typing import Dict, List

from agent import Agent


class Driver:
    __Q_path = "mab\\training_data\\Q.json"
    __num_games_path = "mab\\training_data\\num_games.json"
    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.05  # Minimum exploration probability -> 5 %
    __decay_per_game = 0.0001  # Minimum exploration ratio reached after 10 000 games

    def __init__(self, num_turns: int, num_players: int,  restart=False):
        # Player number corresponds to who starts first, so Player1 plays turn 1
        self.__agents = {agent_index: Agent(num_turns) for agent_index in range(num_players)}
        self.__explore_prob: float = 1.0
        self.__exploring: bool = True
        if not restart:
            self.__continue_training()

    def get_game_actions(self) -> Dict[str, Dict[str, tuple]]:
        return self.explore_actions() if self.__exploring else self.exploit_actions()

    def register_winner(self, winner_index: int) -> None:
        for agent_index, agent in self.__agents.items():
            if agent_index == winner_index:
                agent.register_reward(1)
            else:
                agent.register_reward(0)
        self.update_exploring()

    def explore_actions(self) -> Dict[str, Dict[str, tuple]]:
        return {name: agent.get_explore_dict() for name, agent in self.__agents.items()}

    def exploit_actions(self) -> Dict[str, Dict[str, tuple]]:
        return {name: agent.get_exploit_dict() for name, agent in self.__agents.items()}

    def update_exploring(self) -> None:
        if self.__explore_prob > Driver.__min_explore_prob:
            self.__explore_prob -= Driver.__decay_per_game
        self.__exploring = rnd.random() < self.__explore_prob

    def __continue_training(self) -> None:
        Q = Driver.load_Q_from_json()
        for name, agent in self.__agents.items():
            agent.set_agent_Q(Q[name])

        num_games = Driver.load_num_games_from_json()
        self.__explore_prob = Driver.calc_explore_prob(num_games)

    def pause_training(self) -> None:
        Q = {name: agent.get_agent_Q() for name, agent in self.__agents.items()}
        Driver.dump_Q_to_json(Q)
        Driver.dump_num_games_to_json(self.__explore_prob)

    @staticmethod
    def calc_explore_prob(num_games: int) -> float:
        total_decay = Driver.__decay_per_game * num_games
        return float(1 - total_decay)

    @staticmethod
    def dump_Q_to_json(Q: Dict[str, Dict[str, Dict[str, List[int]]]]) -> None:
        # Q = {agent_index: {bandit_name: {action_combo: [rewards]}}}
        with open(Driver.__Q_path, 'w') as file:
            json.dump(Q, file)

    @staticmethod
    def dump_num_games_to_json(explore_prob) -> None:
        num_games = int((Driver.__max_explore_prob - explore_prob) / Driver.__decay_per_game)
        with open(Driver.__num_games_path, 'w') as file:
            json.dump(num_games, file)

    @staticmethod
    def load_Q_from_json() -> Dict[str, Dict[str, Dict[str, List[int]]]]:
        with open(Driver.__Q_path, 'r') as file:
            Q = json.load(file)
        return Q

    @staticmethod
    def load_num_games_from_json() -> int:
        with open(Driver.__num_games_path, 'r') as file:
            num_games = json.load(file)
        return num_games
