'''
Defines functions to run payloads.
'''

import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from time import sleep


def lockScreenAwarnessWindows() -> None:
    '''
    Run a lock screen awarness payload for Windows.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(1)
    keyboard.send(Keycode.GUI, Keycode.R)
    sleep(0.1)
    keyboard_layout.write('https://eyelockmyscreen.com/\n')
    sleep(0.5)
    keyboard.send(Keycode.F11)


def lockScreenAwarnessLinux(kdePlasma: bool) -> None:
    '''
    Run a lock screen awarness payload for Linux.
    :param bool kdePlasma: True for Kde Plasma system,
    False for Gnome/Xfce/Cinnamon systems.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(1)
    if (kdePlasma):
        keyboard.send(Keycode.ALT, Keycode.SPACE)
    else:
        keyboard.send(Keycode.ALT, Keycode.F2)
    sleep(0.1)
    keyboard_layout.write('xdg-open https://eyelockmyscreen.com/\n')
