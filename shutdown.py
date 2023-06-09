import time
import subprocess
from pynput import keyboard
import threading

# Define the key and the duration for power down
power_down_key = keyboard.KeyCode.from_char('p')
power_down_duration = 2.5  # in seconds

# Variable to keep track of key press
key_pressed = False
start_time = 0


def on_press(key):
    global key_pressed
    global start_time
    if key == power_down_key:
        if not key_pressed:
            key_pressed = True
            start_time = time.time()
            threading.Thread(target=check_duration).start()


def on_release(key):
    global key_pressed
    if key == power_down_key:
        key_pressed = False


def check_duration():
    global start_time
    global key_pressed
    while key_pressed:  # While the key is being pressed
        elapsed_time = time.time() - start_time
        if elapsed_time >= power_down_duration:
            print("Powering down...")
            subprocess.call(['sudo', 'shutdown', '-P', 'now'])
        time.sleep(0.1)  # This delay can be adjusted as per your need

    # This part will be executed if the key is released, to check if it was pressed long enough
    elapsed_time = time.time() - start_time
    if elapsed_time >= power_down_duration:
        print("Powering down...")
        subprocess.call(['sudo', 'shutdown', '-P', 'now'])


# Create a listener for key press and release events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the script running until interrupted
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    listener.stop()
