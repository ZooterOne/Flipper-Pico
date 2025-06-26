import board

from digitalio import DigitalInOut, Pull
from storage import disable_usb_drive

BUTTON_PRESSED_STATE = False

joystick_button = DigitalInOut(board.GP3)
joystick_button.switch_to_input(pull=Pull.UP)
if (joystick_button.value != BUTTON_PRESSED_STATE):
    disable_usb_drive()
