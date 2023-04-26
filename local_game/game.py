from typing import Dict

from player.bot_player import BotPlayer
from player.player import Player


class Game:
    def __init__(self, num_turns: int = 15, num_players: int = 3, graphics: bool = True) -> None:

        self.__num_players: int = num_players
        self.__players: Dict[int, Player] = self.__make_players()
        self.__winner_idx: int = -1
        self.__num_turns: int = num_turns
        self.__graphics: bool = graphics

    def __make_players(self) -> Dict[int, Player]:
        for i in range(self.__num_players):
            self.__players[i] = BotPlayer(i)

    def run(self) -> None:

        turn = 1
        winner = None
        while not winner and turn <= self.__num_turns:
            player_idx = (turn - 1) % self.__num_players
            player = self.__players[player_idx]
            print(f"Current turn: {turn}, current player: {player_idx}")
            player.register_turn()
            player.run()
            if player.is_winner():
                winner = player
            turn += 1

        max_dp = -1
        if not winner:
            for i, player in self.__players.items():
                dp = player.get_damage_points()
                if dp > max_dp:
                    winner = player
                    max_dp = dp
                elif dp == max_dp:
                    winner = None

        if winner:
            self.__winner_idx = winner.get_index()

    def get_winner_index(self):
        return self.__winner_idx
