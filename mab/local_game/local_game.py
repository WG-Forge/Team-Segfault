from typing import Dict, Type, Union

from data.data_io import DataIO
from src.game_map.map import Map
from .local_players.local_bot_player import LocalBotPlayer


class LocalGame:
    GameActions = Type[Dict[int, Dict[str, str]]]

    def __init__(self, game_actions: GameActions, num_turns: int = 15) -> None:
        self.__winner_index = None
        self.__run(game_actions, num_turns)

    def __run(self, game_actions: GameActions, num_turns: int, num_players=3) -> None:
        players: Dict[int, LocalBotPlayer] = {i: LocalBotPlayer(i, game_actions[i]) for i in range(num_players)}

        game_map = Map(DataIO.load_client_map(), DataIO.load_game_state())
        for player in players.values():
            player.add_map(game_map)

        turn, winner = 1, None
        while not winner and turn <= num_turns:
            player_idx = (turn - 1) % num_players
            player = players[player_idx]
            player.register_turn()
            player.run()

            if player.is_winner():
                winner = player
            turn += 1

        max_dp = -1
        if not winner:
            for i, player in players.items():
                dp = player.get_damage_points()
                if dp > max_dp:
                    winner = player
                    max_dp = dp
                elif dp == max_dp:
                    winner = None

        if winner:
            self.__winner_index = winner.get_index()
            print(' Winner player:', self.__winner_index)
        else:
            print(' Draw')

    def get_winner_index(self) -> Union[int, None]:
        return self.__winner_index
