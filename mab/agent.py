from typing import Dict, List

from bandit import Bandit


class Agent:
    __bandit_names = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')

    def __init__(self, num_turns: int):
        self.__bandits = {name: Bandit(num_turns) for name in Agent.__bandit_names}

    def register_reward(self, reward: int) -> None:
        for bandit in self.__bandits.values():
            bandit.register_reward(reward)

    def get_explore_dict(self) -> Dict[str, tuple]:
        return {name: bandit.get_explore_arms() for name, bandit in self.__bandits.items()}

    def get_exploit_dict(self) -> Dict[str, tuple]:
        return {name: bandit.get_exploit_arms() for name, bandit in self.__bandits.items()}

    def set_agent_Q(self, agent_Q: Dict[str, Dict[str, List[int]]]) -> None:
        for name, bandit_Q in agent_Q.items():
            self.__bandits[name].set_bandit_Q(bandit_Q)

    def get_agent_Q(self) -> Dict[str, Dict[str, List[int]]]:
        return {name: bandit.get_bandit_Q() for name, bandit in self.__bandits.items()}
