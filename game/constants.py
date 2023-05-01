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

HEX_RADIUS_X = [-1]
HEX_RADIUS_Y = [-1]

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

MENU_TEXT_COLOR = (159, 255, 25)
MENU_SELECTED_TEXT_COLOR = (48, 240, 144)
MENU_BACKGROUND_TEXT_COLOR = (0, 0, 255, 128)
MENU_BACKGROUND_COLOR = (62, 62, 66, 192)

# player names
PLAYER_NAMES = ['Playa', 'Bot 1', 'Bot 2', 'Bot 3']

# sound options
SOUND_VOLUME = [0.0]

# sound paths
EXPLOSION_SOUND = 'game/assets/sounds/explosion.mp3'
BULLET_SOUND = 'game/assets/sounds/shot.mp3'

# font paths
MENU_FONT = 'game/assets/menu/8-BIT WONDER.TTF'

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

MENU_BACKGROUND_IMAGE = 'game/assets/menu/background.jpg'
GUI_ICON_PATH = 'game/assets/icon.png'
TRACKS_IMAGE_PATH = 'game/assets/tracks.png'

# other
BULLET_VECTOR = (1, 0)
# position of menus in %, relative to the window size
MENU_POSITION = (0, 100)
