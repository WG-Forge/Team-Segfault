from enum import StrEnum


class GameType(StrEnum):
    SINGLE_PLAYER = 'Local singleplayer'
    LOCAL_MULTIPLAYER = 'Local multiplayer'
    PVP_MULTIPLAYER = 'PvP'
    SPECTATE = 'Spectate'
