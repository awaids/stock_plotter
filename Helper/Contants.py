import os, datetime, pygame
# Color
GREEN = (51, 204, 51)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (51, 51, 0)
BOARD_BACKGROUND_COLOR = (25, 49, 94)

# Display
DISPLAY_X = 1000
DISPLAY_Y = 800
DISPLAY_Y_GAP = (0, 0)    # Pixel to leave as gap from (bottom, top)

# Candle data
CANDLE_WIDTH = 5
INTER_CANDLE_GAP = 2

# deduced candle constants
CANDLE_Y_SCLAE = DISPLAY_Y - 100
USEABLE_X_SCREEN = DISPLAY_X - 200
MAX_CANDLES_ON_DISPLAY = int(USEABLE_X_SCREEN/(CANDLE_WIDTH + INTER_CANDLE_GAP ))
USEABLE_Y_SCREEN = DISPLAY_Y - DISPLAY_Y_GAP[0] - DISPLAY_Y_GAP[1]


# Paths
BEGIN_TIME = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
SAVED_NETS = os.path.join(os.path.dirname(__file__), '..', 'SavedNets')
NEW_NET = os.path.join(SAVED_NETS, BEGIN_TIME)