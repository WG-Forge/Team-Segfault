from enum import StrEnum


class GameType(StrEnum):
    LOCAL_MULTIPLAYER = 'Multiplayer'
    SINGLE_PLAYER = 'Local'
    PVP_MULTIPLAYER = 'PvP'
    SPECTATE = 'Spectate'
