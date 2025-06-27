'''
Flipper Pico
------------
Flipper Zero features on a Raspberry Pi Pico.
'''

import menu
import payloads
import PicoLCD
import scanNetworks
import wifiAP

from os import getenv
from terminalio import FONT
from time import sleep


def scanNetworksAction() -> None:
    global TEXT_FONT
    global picoLCD
    scanNetworks.displayAvailableNetworks(picoLCD, font=TEXT_FONT)


def mockKnownAPAction() -> None:
    global TEXT_FONT
    global picoLCD
    wifiAP.setupAP(getenv('KNOWN_WIFI_AP_SSID'), picoLCD, font=TEXT_FONT)
    

def lockScreenAwarenessWindows() -> None:
    payloads.lockScreenAwarnessWindows()


def lockScreenAwarenessGnome() -> None:
    payloads.lockScreenAwarnessLinux(False)


def lockScreenAwarenessPlasma() -> None:
    payloads.lockScreenAwarnessWindows(True)


def lockScreenAwareness() -> None:
    global TEXT_FONT
    global picoLCD
    MENU_WAIT_TIME = 0.5
    sleep(MENU_WAIT_TIME)
    menus = [('Windows', lockScreenAwarenessWindows),
             ('Gnome/Xfce/Cinnamon', lockScreenAwarenessGnome),
             ('Plasma', lockScreenAwarenessPlasma)]
    menu.runMenu(menus, picoLCD, TEXT_FONT)


TEXT_FONT = FONT

picoLCD = PicoLCD.LCD(color=0x001155)
picoLCD.setTitle('Flipper Pico', 0xFFFFFF, TEXT_FONT)
menus = [('Scan available networks', scanNetworksAction),
         ('Mock & monitor known Wifi AP', mockKnownAPAction),
         ('Lock screen awarness', lockScreenAwareness)]
menu.runLoop(menus, picoLCD, TEXT_FONT)
