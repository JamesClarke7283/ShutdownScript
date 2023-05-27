import time
import subprocess
from pynput import keyboard

# Define the key and the duration for power down
key = keyboard.KeyCode.from_char('p')
power_down_duration = 2.5  # in seconds

# Variable to keep track of key press
key_pressed = False
start_time = 0


def on_press(key):
    global key_pressed
    global start_time
    if key == key:
        if not key_pressed:
            key_pressed = True
            start_time = time.time()
            while key_pressed:  # While the key is being pressed
                elapsed_time = time.time() - start_time
                if elapsed_time >= power_down_duration:
                    print("Powering down...")
                    subprocess.call(['sudo', 'shutdown', '-P', 'now'])
                time.sleep(0.1)  # This delay can be adjusted as per your need


def on_release(key):
    global key_pressed
    if key == key:
        key_pressed = False
        print("Key released before the specified duration.")


# Create a listener for key press and release events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the script running until interrupted
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    listener.stop()
