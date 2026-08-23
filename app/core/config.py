from pathlib import Path

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
TEXT_SCALE = 1

# Default device typeface. Users can override this from Settings > Device Font.
FONT_PATH = str(
    Path(__file__).resolve().parents[2] / "assets" / "fonts" / "Sourcerer-Regular.ttf"
)
# Logical point sizes for each UI role.  Adjust these before changing
# TEXT_SCALE when only one part of the interface needs to change.
FONT_SIZE_STATUS = 14
FONT_SIZE_MENU_TITLE = 18
FONT_SIZE_MENU_ITEM = 14
FONT_SIZE_MENU_FOOTER = 14
FONT_SIZE_SCREEN_TITLE = 18
FONT_SIZE_SCREEN_BODY = 14
FONT_SIZE_READER = 16
FONT_SIZE_READER_FOOTER = 14

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


