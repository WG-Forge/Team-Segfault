import random
from threading import Semaphore
from typing import List

from players.player import Player
from players.player_factory import PlayerFactory, PlayerTypes
from players.remote_player import RemotePlayer
from remote.game_client import GameClient


class PlayerManager:
    """" Manages player connections and synchronization """

    def __init__(self, game, shadow_client: GameClient):
        # game container
        self.__game = game
        self.__shadow_client = shadow_client

        self.__lobby_players: int = 0
        self.__num_players: int = 0

        self.__turn_played_sem: Semaphore = Semaphore(0)

        self.__players_queue: List[Player] = []

    def notify_all_players(self) -> None:
        # release all players using their private semaphores
        for player in self.__game.active_players.values():
            player.next_turn_sem.release()

    def handle_player_turns(self) -> None:
        self.notify_all_players()

        # if current player isn't a remote player, end the turn
        if not isinstance(self.__game.current_player, RemotePlayer) and not self.__game.over.is_set():
            self.__shadow_client.force_turn()

        # wait for everyone to finish their turns
        for _ in range(self.__num_players):
            self.__turn_played_sem.acquire()

    def connect_remote_players(self, players: dict) -> None:
        for player in players:
            if player["idx"] not in self.__game.active_players and not player["is_observer"]:
                self.__add_remote_player(player)

    def connect_queued_players(self) -> None:
        for player in self.__players_queue:
            self.__connect_local_player(player)

    def add_local_player(self, name: str, password: str | None = None, is_observer: bool | None = None) -> None:
        """
        Will connect the player if game has started.
        If the game is full, player will be connected as an observer.
        """
        if self.__lobby_players >= self.__game.max_players:
            is_observer = True

        if not is_observer:
            self.__lobby_players += 1

        self.__num_players += 1

        player: Player
        player_type: PlayerTypes
        if is_observer:
            player_type = PlayerTypes.Observer
        else:
            player_type = PlayerTypes.Bot

        player = PlayerFactory.create_player(player_type=player_type,
                                             name=name,
                                             password=password,
                                             is_observer=is_observer,
                                             turn_played_sem=self.__turn_played_sem,
                                             current_player_idx=self.__game.current_player_idx,
                                             player_index=self.__lobby_players - 1,
                                             over=self.__game.over)

        if self.__game.started:
            self.__connect_local_player(player)
        else:
            self.__players_queue.append(player)

    def login(self) -> None:
        self.__shadow_client.login(name=f"{self.__game.game_name}-Team-Segfault-Shadow-{random.randint(0, 100000)}",
                                   game_name=self.__game.game_name,
                                   num_turns=self.__game.num_turns,
                                   num_players=self.__game.max_players,
                                   is_observer=True)

    def logout(self) -> None:
        # end by logging out of the shadow observer
        self.__shadow_client.logout()
        self.__shadow_client.disconnect()

    def __add_remote_player(self, user_info: dict) -> None:
        if not user_info["is_observer"]:
            self.__lobby_players += 1

        self.__num_players += 1

        player: Player = PlayerFactory.create_player(player_type=PlayerTypes.Remote,
                                                     turn_played_sem=self.__turn_played_sem,
                                                     current_player_idx=self.__game.current_player_idx,
                                                     player_index=self.__lobby_players - 1,
                                                     over=self.__game.over)

        self.__connect_remote_player(player, user_info)

    def __connect_local_player(self, player: Player) -> None:
        game_client: GameClient = GameClient()
        user_info: dict = game_client.login(player.player_name, player.password,
                                            self.__game.game_name, self.__game.num_turns,
                                            self.__game.max_players, player.is_observer)

        player.add_to_game(user_info, game_client)
        player.start()

        self.__game.active_players[player.idx] = player

    def __connect_remote_player(self, player: Player, user_info: dict) -> None:
        player.add_to_game(user_info, self.__shadow_client)
        player.start()

        self.__game.active_players[player.idx] = player
