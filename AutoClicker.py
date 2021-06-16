import time
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Controller as MouseController

mouse = MouseController()
keyboard = KeyController()

time.sleep(5)

while 1:
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)

    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)

    time.sleep(15)
