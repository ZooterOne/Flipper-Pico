<h1 align="center">Flipper Pico</h1>

# :thinking: About

Reproduce some of the Flipper Zero features using a Raspberry Pi Pico.

# :bulb: Details

The aim of the project is to use the Raspberry Pi Pico with the addition of a screen and some input buttons and to implement some features from the [Flipper Zero](https://flipper.net/), to see how easy it is to use such device for ethical hacking.

Considering the hardware limitation of the Raspberry Pi Pico, the main feature to be implemented is the ability to run a Bad USB Attack.

Using a Raspberry Pi Pico W, another interesting feature to implement is to fake a known Wifi network and see if any device would automatically connect to it. As a starting point we could implement a Wifi network detection feature.

# :memo: Implementation

Hardware:

 * [Raspberry Pi Pico WH](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html).
 * [Waveshare Pico LCD 1.14](https://www.waveshare.com/wiki/Pico-LCD-1.14).

 Software:

  * [Circuit Python](https://circuitpython.org/).
  * Circuit Python libraries for the Pico LCD and the USB HID.
  * [Thonny IDE](https://thonny.org/).

Features:

 * Press joystick during boot to show the Raspberry Pi Pico as an USB drive _(default behaviour of the board, disabled by our program to enable USB HID for Bad USB Attacks)_.
 * Joystick to navigate through the menu and A button to validate, B button to go back.
 * Scan available Wifi networks _(2.4 GHz only, Raspberry Pi Pico limitation)_, including signal strength.
 * Mock a known Wifi Access Point and monitor all connections.
 * A playful Bad USB attack to [show how important it is to lock screen](https://eyelockmyscreen.com/).
 * Reverse shell Bad USB Attack.

# :computer: Setup

 1. Download the latest stable [Circuit Python for Raspberry Pi Pico W](https://circuitpython.org/board/raspberry_pi_pico_w/).
 2. Follow the [instructions](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython) to install Circuit Python on the Raspberry Pi Pico.
 3. Download latest [Circuit Python libraries bundle](https://circuitpython.org/libraries).
 4. Unzip the bundle file and from Thonny, drag & drop the following files or folders to the Raspberry Pi Pico to install the necessary libraries:
     - `adafruit_displayio_layout`.
     - `adafruit_display_shapes`.
     - `adafruit_display_text`.
     - `adafruit_hid`.
     - `adafruit_st7789.mpy`.
 5. Clone the repository: `git clone https://github.com/ZooterOne/Flipper-Pico`.
 6. From Thonny, drag & drop all the **.py** and **.toml** files from the repository to the Raspberry Pi Pico.
 7. Update **settings.toml** with known Wifi Access Point to mock, and reverse shell listener IP address.
 8. Setup your reverse shell listener if needed (_you should know how to do this_).
 9. Plug the Raspberry Pi Pico to a power source or target computer. 

# :pager: Demo

![](FlipperPicoDemo.gif)
