#
#   DISPLAY
#

SCREEN_WIDTH = 240

SCREEN_HEIGHT = 416

#
#   TYPOGRAPHY
#

# Multiplier applied to every e-reader font.  This is the one setting to
# change when moving to a display with a different pixel density.  For
# example, use 1.25 to make all text 25% larger.
TEXT_SCALE = 1.15

# Set this to a .ttf/.ttc/.otf file to use a specific typeface.  Leave it as
# None to use the first suitable system font found by the display module.
FONT_PATH = None

#
#   I2C
#

I2C_BUS = 1

# Default I2C address for the Adafruit seesaw encoder
ENCODER_I2C_ADDRESS = 0x49

# 
#   INPUT
# 

ROTATION_STEP = 1

LONG_PRESS_TIME = 0.75

DOUBLE_CLICK_TIME = 0.35

ROTARY_PIN_A = 2

ROTARY_PIN_B = None
BUTTON_SELECT = None
REFRESH_RATE = None
# 
#   FILES
# 

BOOK_FOLDER = "books"

DATABASE_PATH = "reader.db"

LOG_PATH = "logs/reader.log"


