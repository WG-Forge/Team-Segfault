# server info
HOST_NAME = "wgforge-srv.wargaming.net"
HOST_PORT = 443

GAME_NAME = ['Test game']

# gui constants
GUI_CAPTION = 'Team Segfault'
FPS_MAX = 30  # max frames per second
SCREEN_SIZE = 250
SCREEN_RATIO = (4, 3)
SCREEN_WIDTH = SCREEN_RATIO[0] * SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_RATIO[1] * SCREEN_SIZE
HEX_RADIUS_X = [-1]
HEX_RADIUS_Y = [-1]
IMAGE_TO_HEX_RAD_RATIO = 1.5
# tank icon for registering non-fatal shot
TANK_SHADOW_ALPHA = 64
TANK_PULSE_FULL_DURATION = 20
TANK_SHADOW_MAX_SCALE = 2.5

MAP_FONT_SIZE_MULTIPLIER = 1.2

# position of menus in %, relative to the window size
MENU_POSITION = (0, 100)
MENU_MIN_WIDTH = SCREEN_WIDTH / 4
TRACKS_SCALE = (SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 10)
LOADING_ANIMATION_LIMIT = 30

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_BACKGROUND = (47, 31, 128)
PLAYER_COLORS = ((224, 206, 70), (70, 191, 224), (201, 26, 40))  # yellow, blue, red
BASE_COLOR = (39, 161, 72)
EMPTY_COLOR = (87, 81, 81)
OBSTACLE_COLOR = (51, 46, 46)
DEFAULT_SPAWN_COLOR = (135, 126, 126)

MENU_TEXT_COLOR = (159, 255, 25)
MENU_SELECTED_TEXT_COLOR = (48, 240, 144)
MENU_BACKGROUND_TEXT_COLOR = (0, 0, 255, 128)
MENU_BACKGROUND_COLOR = (62, 62, 66, 192)

LOADING_BAR_COLOR = (55, 84, 38)

# player names
PLAYER_NAMES = ['Playa', 'Bot 1', 'Bot 2', 'Bot 3']

# game options
# game speed range is [0.0 - 1.0]; represents (1 - game_speed) seconds sleep between turns
GAME_SPEED = [1.0]
SOUND_VOLUME = [0.0]

# sound paths
EXPLOSION_SOUND = 'game/assets/sounds/explosion.mp3'
BULLET_SOUND = 'game/assets/sounds/shot.mp3'

# font paths
MENU_FONT = 'game/assets/menu/BrunoAceSC-Regular.ttf'

# image paths
TANK_ICON_PATH = 'game/assets/tank_icon.png'
SPG_IMAGE_PATH = 'game/assets/tank_classes/spg.png'
HT_IMAGE_PATH = 'game/assets/tank_classes/ht.png'
LT_IMAGE_PATH = 'game/assets/tank_classes/lt.png'
MT_IMAGE_PATH = 'game/assets/tank_classes/mt.png'
TD_IMAGE_PATH = 'game/assets/tank_classes/td.png'

CATAPULT_IMAGE_PATH = 'game/assets/local_bonuses/catapult.png'
LIGHT_REPAIR_IMAGE_PATH = 'game/assets/local_bonuses/light_repair.png'
HARD_REPAIR_IMAGE_PATH = 'game/assets/local_bonuses/hard_repair.png'

FLAG_PATH = 'game/assets/flag.png'
EXPLOSION_IMAGES = [f'game/assets/explosion_images/{i}.png' for i in range(7)]
BULLET_IMAGE_PATH = 'game/assets/white_bullet.png'

MENU_BACKGROUND_IMAGE = 'game/assets/menu/background.jpg'
GUI_ICON_PATH = 'game/assets/icon.png'
TRACKS_IMAGE_PATH = 'game/assets/tracks.png'

# other
BULLET_VECTOR = (1, 0)
