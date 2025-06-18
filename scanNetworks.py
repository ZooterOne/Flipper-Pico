'''
Defines functions to use scan networks and display results.
'''

import PicoLCD
import fontio

from displayio import Group
from terminalio import FONT
from wifi import radio, AuthMode

from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label


def __getAvailableNetworks(openNetworksOnly: bool) -> List[(str, int)]:
    '''
    Get a list of available networks as (ssid, signal strength).
    :param bool openNetworksOnly: only get Open networks.
    :return: list of available networks as (ssid, signal strength).
    :rtype: List[(str, int)]
    '''
    scanned_networks = {}
    radio.enabled = True
    for network in radio.start_scanning_networks():
        if not network.ssid:
            continue
        if openNetworksOnly and not AuthMode.OPEN in network.authmode:
            continue
        value = network.rssi if network.ssid not in scanned_networks else max(scanned_networks[network.ssid], network.rssi)
        scanned_networks[network.ssid] = value
    radio.stop_scanning_networks()
    sorted_networks = sorted(list(scanned_networks.items()), key=lambda item: item[1], reverse=True)
    radio.enabled = False
    return sorted_networks


def __generateCells(networks: List[(str, int)],
                    font: fontio.FontProtocol) -> List[(label.Label, Rect)]:
    '''
    Generates the grid cells with network data.
    :param List[(str, int)] networks: list of networks to display.
    :param fontio.FontProtocol font: the font to use to display text.
    :return: list of grid cells.
    :rtype: List[(label.Label, Rect)]
    '''
    GOOD_SIGNAL_LOWER_LIMIT = -80
    BAD_SIGNAL_UPPER_LIMIT = -67
    cells = []
    for ssid, rssi in networks:
        label_ssid = label.Label(font, text=ssid, color=0xFFFFFF)
        color = 0x00FF00
        if rssi <= GOOD_SIGNAL_LOWER_LIMIT:
            color = 0xFF0000
        elif rssi < BAD_SIGNAL_UPPER_LIMIT:
            color = 0xFFFF00
        rect_signal = Rect(0, 0, label_ssid.height, (3 * label_ssid.height) // 4,
                           fill=color, outline=None)
        cells.append((label_ssid, rect_signal))
    return cells


def __displayNetworks(networks: List[(str, int)],
                      picoLCD: PicoLCD.LCD,
                      display: Group,
                      font: fontio.FontProtocol) -> None:
    '''
    Display a list of network to the given screen.
    :param List[(str, int)] networks: list of networks to display.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param Group display: the group to attach the display data to.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    cells = __generateCells(networks, font)
    CELL_MARGIN = 2
    max_cell_height = font.get_bounding_box()[1] + 2 * CELL_MARGIN
    margin = font.get_bounding_box()[1] // 2
    max_row_count = (picoLCD.height_without_title - margin * 2) // max_cell_height
    row_count = min(max_row_count, len(cells))
    col_count = (PicoLCD.WIDTH - margin * 2) // (max_cell_height * 2)
    grid = GridLayout(
        x = margin,
        y = margin,
        width = PicoLCD.WIDTH - margin * 2,
        height = max_cell_height * row_count,
        grid_size = (col_count, row_count),
        divider_lines = True,
        cell_anchor_point = (0.5,0.5)
    )
    for row_index in range(0, row_count):
        grid.add_content(cells[row_index][0],
                         grid_position=(0, row_index),
                         cell_size=(col_count - 1, 1))
        grid.add_content(cells[row_index][1],
                         grid_position=(col_count - 1, row_index),
                         cell_size=(1, 1))
    display.append(grid)


def displayAvailableNetworks(picoLCD: PicoLCD.LCD,
                             font: fontio.FontProtocol=FONT) -> None:
    '''
    Detect and display a list of available networks.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    while True:
        networks = __getAvailableNetworks(False)
        display = Group(x=0,
                        y=PicoLCD.HEIGHT - picoLCD.height_without_title)
        picoLCD.screen.append(display)
        if len(networks) == 0:
            message = label.Label(font, text='No network detected.', color=0xFFFFFF)
            message.anchor_point = (0.5, 0)
            message.anchored_position = (PicoLCD.WIDTH // 2, font.get_bounding_box()[1])
            display.append(message)
        else:
            __displayNetworks(networks, picoLCD, display, font)
        while True:
            if picoLCD.isBackButtonPressed():
                picoLCD.screen.remove(display)
                picoLCD.refresh(display.x, display.y,
                                PicoLCD.WIDTH, picoLCD.height_without_title)
                return
            if picoLCD.isActionButtonPressed():
                break
        picoLCD.screen.remove(display)
        picoLCD.refresh(display.x, display.y,
                        PicoLCD.WIDTH, picoLCD.height_without_title)
