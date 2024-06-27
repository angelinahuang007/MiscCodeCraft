import tkinter as tk
import pynput
from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Controller, Button

# Create the main window
root = tk.Tk()
root.title("Mouse Clicker")

# Mouse controller for clicking
mouse = Controller()

clicking = False

def on_press(key):
    # Check if F8 is pressed
    if key == Key.f8:
        global clicking
        if not clicking:
            start_clicking()
        else:
            stop_clicking()

def start_clicking():
    global clicking
    clicking = True
    click_continuously()

def stop_clicking():
    global clicking
    clicking = False

def click_continuously():
    if clicking:
        mouse.click(Button.left, 1)  # Correct usage
        root.after(100, click_continuously)  # Adjust the delay as necessary

# Start the keyboard listener
keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

# Start the GUI event loop
root.mainloop()
