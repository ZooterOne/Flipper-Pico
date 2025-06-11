import menu
import PicoLCD
'''
Flipper Pico
------------
Flipper Zero features on a Raspberry Pi Pico.
'''

import scanNetworks

from terminalio import FONT


def scanNetworksAction() -> None:
    global TEXT_FONT
    global picoLCD
    scanNetworks.displayAvailableNetworks(picoLCD, font=TEXT_FONT)


TEXT_FONT = FONT

picoLCD = PicoLCD.LCD(color=0x001155)
picoLCD.setTitle('Flipper Pico', 0xFFFFFF, TEXT_FONT)
menus = [('Scan available networks', scanNetworksAction)]
menu.run(menus, picoLCD, TEXT_FONT)