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

# Set this to a .ttf/.ttc/.otf file to use a specific typeface.  Leave it as
# None to use the first suitable system font found by the display module.
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
# Logical point sizes for each UI role.  Adjust these before changing
# TEXT_SCALE when only one part of the interface needs to change.
FONT_SIZE_STATUS = 14
FONT_SIZE_MENU_TITLE = 24
FONT_SIZE_MENU_ITEM = 20
FONT_SIZE_MENU_FOOTER = 18
FONT_SIZE_SCREEN_TITLE = 22
FONT_SIZE_SCREEN_BODY = 18
FONT_SIZE_READER = 26
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


