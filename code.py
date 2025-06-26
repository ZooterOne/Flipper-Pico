'''
Flipper Pico
------------
Flipper Zero features on a Raspberry Pi Pico.
'''

import menu
import PicoLCD
import scanNetworks
import wifiAP

from os import getenv
from terminalio import FONT


def scanNetworksAction() -> None:
    global TEXT_FONT
    global picoLCD
    scanNetworks.displayAvailableNetworks(picoLCD, font=TEXT_FONT)


def mockKnownAPAction() -> None:
    global TEXT_FONT
    global picoLCD
    wifiAP.setupAP(getenv('KNOWN_WIFI_AP_SSID'), picoLCD, font=TEXT_FONT)


TEXT_FONT = FONT

picoLCD = PicoLCD.LCD(color=0x001155)
picoLCD.setTitle('Flipper Pico', 0xFFFFFF, TEXT_FONT)
menus = [('Scan available networks', scanNetworksAction),
         ('Mock & monitor known Wifi AP', mockKnownAPAction)]
menu.run(menus, picoLCD, TEXT_FONT)
