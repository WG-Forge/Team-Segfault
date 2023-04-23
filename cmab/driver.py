import json
import random as rnd
from typing import Dict, List, Tuple

from agent import Agent


class Driver:
    __Q_path = "cmab\\training_data\\Q.json"
    __num_games_path = "cmab\\training_data\\num_games.json"
    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.05  # Minimum exploration probability -> 5 %
    __decay_per_game = 0.0001  # Minimum exploration ratio reached after 10 000 games

    def __init__(self, num_turns: int, agent_names: tuple, restart=False):
        # Player number corresponds to who starts first, so Player1 plays turn 1
        self.__agent_names = agent_names
        self.__agents = {name: Agent(name, num_turns) for name in agent_names}
        self.__explore_prob: float = 1.0
        self.__exploring: bool = True
        if not restart:
            self.__continue_training()

    def get_game_actions(self) -> Dict[str, Dict[str, tuple]]:
        return self.explore_actions() if self.__exploring else self.exploit_actions()

    def register_game_results(self, winner_name: str, game_actions: Dict[str, Dict[str, tuple]]) -> None:
        for name, actions in game_actions.items():
            self.__agents[name].register_reward(winner_name, game_actions[name])
        self.update_exploring()

    def explore_actions(self) -> Dict[str, Dict[str, tuple]]:
        return {name: agent.get_explore_dict() for name, agent in self.__agents.items()}

    def exploit_actions(self) -> Dict[str, Dict[str, tuple]]:
        return {name: agent.get_exploit_dict() for name, agent in self.__agents.items()}

    def update_exploring(self) -> None:
        if self.__explore_prob > Driver.__min_explore_prob:
            self.__explore_prob -= Driver.__decay_per_game
        self.__exploring = rnd.random() < self.__explore_prob

    def get_turn_actions_for(self, player_index: int) -> Dict[str, str]:
        agent_name = self.__agent_names[player_index]
        agent = self.__agents[agent_name]
        return agent.get_turn_actions(self.__exploring)

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
