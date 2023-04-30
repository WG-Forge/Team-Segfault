from players.player import Player


class Observer(Player):

    def _make_turn_plays(self) -> None:
        # force next turn
        self._game_client.force_turn()

    def _finalize(self) -> None:
        self._game_client.logout()
        self._game_client.disconnect()
