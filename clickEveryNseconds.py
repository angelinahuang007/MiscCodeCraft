import pyautogui
import time
import keyboard

print("Press 's' to start the automatic clicking. Press 'q' to stop.")

# Wait until 's' is pressed to start
keyboard.wait('s')

try:
    while True:
        pyautogui.click()  # Clicks at the current mouse position
        print("Clicked")
        time.sleep(61)     # Waits for 61 seconds before the next click
        if keyboard.is_pressed('q'):  # Checks if 'q' is pressed to exit
            print("Exiting...")
            break
except KeyboardInterrupt:
    print("Program forcibly stopped.")
