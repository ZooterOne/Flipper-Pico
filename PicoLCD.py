'''
Defines class and functions to use Pico LCD 1.14.
https://www.waveshare.com/wiki/Pico-LCD-1.14
'''

import board
import fontio

from busio import SPI
from digitalio import DigitalInOut, Pull
from displayio import Bitmap, Group, Palette, TileGrid, release_displays
from fourwire import FourWire
from terminalio import FONT
from adafruit_display_text import label
from adafruit_st7789 import ST7789


# Declare all pins (see https://www.waveshare.com/wiki/Pico-LCD-1.14)
LCD_DC = board.GP8
LCD_CS = board.GP9
LCD_CLK = board.GP10
LCD_DIN = board.GP11
LCD_RST = board.GP12
LCD_BL = board.GP13
UP = board.GP2
DOWN = board.GP18
LEFT = board.GP16
RIGHT = board.GP20
CTRL = board.GP3
A = board.GP15
B = board.GP17

# Declare constants
WIDTH = 240
HEIGHT = 135
BUTTON_PRESSED_STATE = False


class LCD():
    def __init__(self, color: int):
        '''
        Setup LCD screen.
        :param int color: background color.
        '''
        # See https://docs.circuitpython.org/projects/st7789/en/latest/examples.html
        release_displays()
        spi = SPI(clock=LCD_CLK, MOSI=LCD_DIN)
        display_bus = FourWire(spi, command=LCD_DC, chip_select=LCD_CS, reset=LCD_RST)
        display = ST7789(display_bus, rotation=270, width=WIDTH, height=HEIGHT,
                         colstart=53, rowstart=40, backlight_pin=LCD_BL)
        self.screen = Group(x=0, y=0)
        display.root_group = self.screen
        self.__background_bitmap = Bitmap(WIDTH, HEIGHT, 1)
        background_palette = Palette(1)
        background_palette[0] = color
        background = TileGrid(self.__background_bitmap,
                              pixel_shader=background_palette,
                              x=0, y=0)
        self.screen.append(background)
        self.height_without_title = HEIGHT
        self.__back_button = DigitalInOut(B)
        self.__back_button.switch_to_input(pull=Pull.UP)
        self.__action_button = DigitalInOut(A)
        self.__action_button.switch_to_input(pull=Pull.UP)


    def setTitle(self, title: str, color: int,
                 font: fontio.FontProtocol=FONT,
                 scale: int=2) -> None:
        '''
        Display given title on screen.
        :param str title: title to display.
        :param int color: title foreground color.
        :param fontio.FontProtocol font: font to use.
        :param int scale: scale to apply.
        '''
        if (self.height_without_title < HEIGHT):
            raise RuntimeError('Title already set.')
        title_label = label.Label(text=title, color=color, font=font, scale=scale)
        title_label.anchor_point = (0.5, 0)
        title_label.anchored_position = (WIDTH // 2, 0)
        self.screen.append(title_label)
        self.height_without_title = self.height_without_title - title_label.height * scale


    def refresh(self, x: int, y: int, width: int, height: int) -> None:
        '''
        Refresh given area.
        :param int x: top-left x position of the area to refresh.
        :param int y: top-left y position of the area to refresh.
        :param int width: width of the area to refresh.
        :param int height: height of the area to refresh.
        '''
        self.__background_bitmap.dirty(x, y, x + width, y + height)
        

    def isBackButtonPressed(self) -> bool:
        '''
        Gets if the back button is currently pressed.
        :return: True if the button is pressed, False otherwise.
        :rtype: bool
        '''
        return self.__back_button.value == BUTTON_PRESSED_STATE
    
    
    def isActionButtonPressed(self) -> bool:
        '''
        Gets if the action button is currently pressed.
        :return: True if the button is pressed, False otherwise.
        :rtype: bool
        '''
        return self.__action_button.value == BUTTON_PRESSED_STATE
