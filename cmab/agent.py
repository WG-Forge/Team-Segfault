from typing import Dict, List

from bandit import Bandit


class Agent:
    __bandit_names = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')

    def __init__(self, name: str, num_turns: int):
        self.__agent_name: str = name
        self.__bandits = {name: Bandit(name, num_turns) for name in Agent.__bandit_names}

    def get_explore_dict(self) -> Dict[str, tuple]:
        return {name: bandit.get_explore_arms() for name, bandit in self.__bandits.items()}

    def get_exploit_dict(self) -> Dict[str, tuple]:
        return {name: bandit.get_exploit_arms() for name, bandit in self.__bandits.items()}

    def set_agent_Q(self, agent_Q: Dict[str, Dict[str, List[int]]]) -> None:
        for name, bandit_Q in agent_Q.items():
            self.__bandits[name].set_bandit_Q(bandit_Q)

    def get_agent_Q(self) -> Dict[str, Dict[str, List[int]]]:
        return {name: bandit.get_bandit_Q() for name, bandit in self.__bandits.items()}

    def register_reward(self, reward: int, game_actions: dict) -> None:
        for name, bandit in self.__bandits.items():
            bandit.register_reward(reward, game_actions[name])

    def register_turn(self, bandit_arms: Dict[str, str]) -> None:
        for bandit_name, arm in bandit_arms.items():
            bandit = self.__bandits[bandit_name]
            bandit.register_turn(arm)
