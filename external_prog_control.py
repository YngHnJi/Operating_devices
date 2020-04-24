# external_prog_control.py
import time
from pywinauto.application import Application
import pyautogui

app = Application().start("C:\Program Files\PuTTY\putty.exe")

target_pos = ((1255, 769), (1433, 745), (1395, 910))
"""
pyautogui.click(target_pos[0][0], target_pos[0][1])
pyautogui.click(target_pos[1][0], target_pos[1][1])
pyautogui.click(target_pos[2][0], target_pos[2][1])
"""
pyautogui.doubleClick(target_pos[0][0], target_pos[0][1])

pyautogui.write("yhji")
pyautogui.press("enter")
time.sleep(3)
pyautogui.write("123213zz")
pyautogui.press("enter")