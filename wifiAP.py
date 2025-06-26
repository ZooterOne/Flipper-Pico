'''
Defines functions to setup Wifi Access Point and display connected devices.
'''

import PicoLCD
import fontio

from displayio import Group
from terminalio import FONT
from wifi import radio

from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label


def __getConnectedDevices() -> List[(str, str)]:
    '''
    Get a list of connected devices as (ip address, mac address).
    :return: list of connected devices as (ip address, mac address).
    :rtype: List[(str, str)]
    '''
    if not radio.ap_active:
        return []
    connected_devices = [(str(device.ipv4_address), device.mac_address.hex(':')) for device in radio.stations_ap]
    return connected_devices


def __generateCells(devices: List[(str, str)],
                    font: fontio.FontProtocol) -> List[(label.Label, label.Label)]:
    '''
    Generates the grid cells with devices data.
    :param List[(str, str)] networks: list of devices to display.
    :param fontio.FontProtocol font: the font to use to display text.
    :return: list of grid cells.
    :rtype: List[(label.Label, label.Label)]
    '''
    cells = []
    for ip_address, mac_address in devices:
        label_ip = label.Label(font, text=ip_address, color=0xFFFFFF)
        label_mac = label.Label(font, text=mac_address, color=0xFFFFFF)
        cells.append((label_ip, label_mac))
    return cells


def __displayDevices(devices: List[(str, str)],
                     picoLCD: PicoLCD.LCD,
                     display: Group,
                     font: fontio.FontProtocol) -> None:
    '''
    Display a list of devices to the given screen.
    :param List[(str, str)] devices: list of devices to display.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param Group display: the group to attach the display data to.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    cells = __generateCells(devices, font)
    CELL_MARGIN = 2
    COL_COUNT = 2
    max_cell_height = font.get_bounding_box()[1] + 2 * CELL_MARGIN
    margin = font.get_bounding_box()[1] // 2
    max_row_count = (picoLCD.height_without_title - margin * 2) // max_cell_height
    row_count = min(max_row_count, len(cells))
    grid = GridLayout(
        x = margin,
        y = margin,
        width = PicoLCD.WIDTH - margin * 2,
        height = max_cell_height * row_count,
        grid_size = (COL_COUNT, row_count),
        divider_lines = True,
        cell_anchor_point = (0.5,0.5)
    )
    for row_index in range(0, row_count):
        grid.add_content(cells[row_index][0],
                         grid_position=(0, row_index),
                         cell_size=(1, 1))
        grid.add_content(cells[row_index][1],
                         grid_position=(1, row_index),
                         cell_size=(1, 1))
    display.append(grid)


def setupAP(ssid: str, picoLCD: PicoLCD.LCD,
            font: fontio.FontProtocol=FONT) -> None:
    '''
    Setup a Wifi Acess Point and monitor connected devices.
    :param str ssid: the ssid to setup.
    :param PicoLCD.LCD picoLCD: the screen to display the data onto.
    :param fontio.FontProtocol font: the font to use to display text.
    '''
    radio.enabled = True
    radio.start_ap(ssid=ssid, password='')
    while True:
        connected_devices = __getConnectedDevices()
        display = Group(x=0,
                        y=PicoLCD.HEIGHT - picoLCD.height_without_title)
        picoLCD.screen.append(display)
        if len(connected_devices) == 0:
            message = label.Label(font, text='No device connected.', color=0xFFFFFF)
            message.anchor_point = (0.5, 0)
            message.anchored_position = (PicoLCD.WIDTH // 2, font.get_bounding_box()[1])
            display.append(message)
        else:
            __displayDevices(connected_devices, picoLCD, display, font)
        while True:
            if picoLCD.isBackButtonPressed():
                picoLCD.screen.remove(display)
                picoLCD.refresh(display.x, display.y,
                                PicoLCD.WIDTH, picoLCD.height_without_title)
                radio.stop_ap()
                radio.enabled = False
                return
            if picoLCD.isActionButtonPressed():
                break
        picoLCD.screen.remove(display)
        picoLCD.refresh(display.x, display.y,
                        PicoLCD.WIDTH, picoLCD.height_without_title)
