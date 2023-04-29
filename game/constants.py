# server info
HOST_NAME = "wgforge-srv.wargaming.net"
HOST_PORT = 443

GAME_NAME = ['Test game ']

# gui constants
FPS_MAX = 30  # max frames per second
SCREEN_SIZE = 250
SCREEN_RATIO = (4, 3)
SCREEN_WIDTH = SCREEN_RATIO[0] * SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_RATIO[1] * SCREEN_SIZE

# this is reduced when on game start
HEX_RADIUS_X = [SCREEN_WIDTH]
HEX_RADIUS_Y = [SCREEN_HEIGHT]

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_BACKGROUND = (47, 31, 128)
PLAYER_COLORS = ((224, 206, 70), (70, 191, 224), (201, 26, 40))  # yellow, blue, red
PLAYER1_COLOR = (224, 206, 70)  # yellow
PLAYER2_COLOR = (70, 191, 224)  # blue
PLAYER3_COLOR = (201, 26, 40)  # red
BASE_COLOR = (39, 161, 72)
EMPTY_COLOR = (87, 81, 81)
OBSTACLE_COLOR = (51, 46, 46)
DEFAULT_SPAWN_COLOR = (135, 126, 126)
MENU_TEXT_COLOR = (231, 252, 3)
MENU_SELECTED_TEXT_COLOR = (252, 186, 3)
MENU_FONT = 'game/assets/menu/8-BIT WONDER.TTF'

# player names
PLAYER_NAMES = ['Playa', 'Bot 1', 'Bot 2', 'Bot 3']

# sound options
SOUND_VOLUME = [1.0]

# sound paths
EXPLOSION_SOUND = 'game/assets/sounds/explosion.mp3'
BULLET_SOUND = 'game/assets/sounds/shot.mp3'

# image paths
TANK_ICON_PATH = 'game/assets/tank_icon.png'
SPG_IMAGE_PATH = 'game/assets/tank_classes/spg.png'
HT_IMAGE_PATH = 'game/assets/tank_classes/ht.png'
LT_IMAGE_PATH = 'game/assets/tank_classes/lt.png'
MT_IMAGE_PATH = 'game/assets/tank_classes/mt.png'
TD_IMAGE_PATH = 'game/assets/tank_classes/td.png'

CATAPULT_IMAGE_PATH = 'game/assets/upgrades/catapult.png'
LIGHT_REPAIR_IMAGE_PATH = 'game/assets/upgrades/light_repair.png'
HARD_REPAIR_IMAGE_PATH = 'game/assets/upgrades/hard_repair.png'

FLAG_PATH = 'game/assets/flag.png'
EXPLOSION_IMAGES = [f'game/assets/explosion/{i}.png' for i in range(7)]
BULLET_IMAGE_PATH = 'game/assets/white_bullet.png'

MENU_IMAGE = 'game/assets/menu/background.jpg'
