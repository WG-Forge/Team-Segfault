from player.player import Player


class Observer(Player):

    def _make_turn_plays(self) -> None:
        # force next turn
        self._game_client.force_turn()
