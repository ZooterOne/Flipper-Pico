'''
Defines functions to display and manage menu.
'''

import PicoLCD
import fontio

from displayio import Group
from terminalio import FONT
from time import sleep

from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_text import label


def __generateMenu(menus: List[(str, Callable)],
                   picoLCD: PicoLCD.LCD,
                   font: fontio.FontProtocol) -> Group:
    '''
    Generates the grid used to display the menu.
    :param List[(str, Callable)] menus: list of menu lines to display.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param fontio.FontProtocol font: the font to use to display text.
    :return: grid with menu lines.
    :rtype: Group
    '''
    CELL_MARGIN = 2
    max_cell_height = font.get_bounding_box()[1] + 2 * CELL_MARGIN
    margin = font.get_bounding_box()[1] // 2
    max_row_count = (picoLCD.height_without_title - margin * 2) // max_cell_height
    row_count = min(max_row_count, len(menus))
    col_count = (PicoLCD.WIDTH - margin * 2) // max_cell_height
    grid = GridLayout(
        x = margin,
        y = margin,
        width = PicoLCD.WIDTH - margin * 2,
        height = max_cell_height * row_count,
        grid_size = (col_count, row_count),
        divider_lines = False,
        cell_anchor_point = (0,0.5)
    )
    grid.add_content(label.Label(font, text='->', color=0xBBFF00),
                     grid_position=(0, 0),
                     cell_size=(1, 1))
    for row_index in range(0, row_count):
        grid.add_content(label.Label(font, text=menus[row_index][0], color=0xFFFFFF),
                         grid_position=(1, row_index),
                         cell_size=(col_count - 1, 1))
    return grid


def runMenu(menus: List[(str, Callable)],
            picoLCD: PicoLCD.LCD,
            font: fontio.FontProtocol) -> None:
    '''
    Run the menu given by a collection of (string, function).
    :param List[(str, Callable)] menus: list of menu lines to display.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    display = Group(x=0,
                    y=PicoLCD.HEIGHT - picoLCD.height_without_title)
    picoLCD.screen.append(display)
    menu_grid = __generateMenu(menus, picoLCD, font)
    active_menu = 0
    display.append(menu_grid)
    BUTTON_WAIT_TIME = 0.25
    while True:
        if picoLCD.isActionButtonPressed():
            picoLCD.screen.remove(display)
            picoLCD.refresh(display.x, display.y,
                            PicoLCD.WIDTH, picoLCD.height_without_title)
            menus[active_menu][1]()
            break
        if picoLCD.isDownButtonPressed():
            arrow = menu_grid.pop_content((0, active_menu))
            active_menu = (active_menu + 1) % len(menus)
            menu_grid.add_content(arrow,
                                  grid_position=(0, active_menu),
                                  cell_size=(1, 1))
            sleep(BUTTON_WAIT_TIME)
        if picoLCD.isUpButtonPressed():
            arrow = menu_grid.pop_content((0, active_menu))
            active_menu = (active_menu - 1) % len(menus)
            menu_grid.add_content(arrow,
                                  grid_position=(0, active_menu),
                                  cell_size=(1, 1))
            sleep(BUTTON_WAIT_TIME)


def runLoop(menus: List[(str, Callable)],
            picoLCD: PicoLCD.LCD,
            font: fontio.FontProtocol=FONT) -> None:
    '''
    Indefinitely run the menu given by a collection of (string, function).
    :param List[(str, Callable)] menus: list of menu lines to display.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    while True:
        runMenu(menus, picoLCD, font)
