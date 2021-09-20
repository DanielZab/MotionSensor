import os
import serial
import time
import win32gui, win32con, win32com.client
from pynput import keyboard

input("Start?")
this_script = win32gui.GetForegroundWindow()
time.sleep(0.1)
win32gui.ShowWindow(this_script, win32con.SW_HIDE)
the_program_to_hide = ""
port = 'COM5'

do_not_force_minimize = ["", "NVIDIA GeForce Overlay", "Malwarebytes Tray Application", "Program Manager"]

# The key combination to check
COMBINATION = {keyboard.Key.alt_gr, keyboard.Key.ctrl_r}

# The currently active modifiers
current = set()
def openFile():
    try:
        global the_program_to_hide
        os.startfile("OrganischeChemie.docx")
        if the_program_to_hide == "":
            time.sleep(3)
            the_program_to_hide = win32gui.GetForegroundWindow()
            
    except Exception as e:
        print(e)
def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd) and all(e != str(win32gui.GetWindowText(hwnd)) for e in do_not_force_minimize):
        win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)
def showFile():
    if the_program_to_hide != "":
        win32gui.ShowWindow(the_program_to_hide , win32con.SW_SHOW)
        openFile()
        cur = win32gui.GetForegroundWindow()
        if cur != the_program_to_hide and str(win32gui.GetWindowText(cur)) != "":
            win32gui.ShowWindow(cur, win32con.SW_FORCEMINIMIZE)
            win32gui.EnumWindows(winEnumHandler, None)


def on_press(key):
    if key == keyboard.Key.esc:
        win32gui.PostMessage(the_program_to_hide,win32con.WM_CLOSE,0,0)
        win32gui.ShowWindow(this_script , win32con.SW_SHOW)
        global q
        q = True
        return False
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            return False
def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

openFile()
q = False
ard = serial.Serial(port,9600,timeout=None)
while True:
    win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
    try:
        ard.read(3)
    except Exception as e:
        win32gui.PostMessage(the_program_to_hide,win32con.WM_CLOSE,0,0)
        print(e)
        break
    showFile()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    if q:
        break
    if ard.in_waiting > 0:
        ard.read(ard.in_waiting)
