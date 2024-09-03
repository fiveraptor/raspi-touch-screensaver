import os
import time
from evdev import InputDevice, categorize, ecodes
from select import select  # Importing the select module

# Path to the brightness file
BRIGHTNESS_FILE = "/sys/class/backlight/10-0045/brightness"
# Brightness values
BRIGHTNESS_ON = "255"
BRIGHTNESS_HALF = "50"
BRIGHTNESS_OFF = "0"
# Time in seconds until the display is half-dimmed
HALF_DIM_TIMEOUT = 600
# Time in seconds until the display is fully dimmed (after half-dimming)
FULL_DIM_TIMEOUT = 1200

# Status to check if the display is dimmed
is_half_dimmed = False
is_fully_dimmed = False

# Function to set the brightness
def set_brightness(value):
    try:
        with open(BRIGHTNESS_FILE, 'w') as f:
            f.write(value)
        print(f"Brightness set to {value}")
    except Exception as e:
        print(f"Error setting brightness: {e}")

# Touchscreen device (this needs to be adjusted depending on your device)
try:
    touchscreen_device = InputDevice('/dev/input/event4')  # Use /dev/input/event6 for your device
    print(f"Touchscreen device found: {touchscreen_device}")
except Exception as e:
    print(f"Error opening touchscreen device: {e}")
    exit(1)

# Time when the last touch event occurred
last_touch_time = time.time()

# Initially set the display to full brightness
set_brightness(BRIGHTNESS_ON)

# Infinite loop that waits for touch events
try:
    while True:
        # Check if an event is present
        r, w, x = select([touchscreen_device.fd], [], [], 1)
        if r:
            for event in touchscreen_device.read():
                if event.type == ecodes.EV_KEY:
                    if is_fully_dimmed:
                        # If the display is fully dimmed, only wake it up
                        last_touch_time = time.time()
                        set_brightness(BRIGHTNESS_ON)
                        is_fully_dimmed = False
                        is_half_dimmed = False
                        touchscreen_device.ungrab()  # Release the touchscreen
                        print("Display fully woke up from dimmed state.")
                    elif is_half_dimmed:
                        # If the display is half-dimmed, just set it to full brightness
                        last_touch_time = time.time()
                        set_brightness(BRIGHTNESS_ON)
                        is_half_dimmed = False
                        print("Display woke up to full brightness.")
                    else:
                        # If the display is already on, process normal touch input
                        last_touch_time = time.time()
                        print(f"Touch event detected at {time.time()}")
                        # Here the browser could receive the input

        # Dim brightness to half if no touch event is detected within HALF_DIM_TIMEOUT
        if not is_half_dimmed and time.time() - last_touch_time > HALF_DIM_TIMEOUT:
            print(f"No touch event detected for {HALF_DIM_TIMEOUT} seconds, dimming display to half brightness.")
            set_brightness(BRIGHTNESS_HALF)
            is_half_dimmed = True

        # Fully dim brightness if no touch event is detected within FULL_DIM_TIMEOUT
        if not is_fully_dimmed and time.time() - last_touch_time > FULL_DIM_TIMEOUT:
            print(f"No touch event detected for {FULL_DIM_TIMEOUT} seconds, dimming display fully.")
            set_brightness(BRIGHTNESS_OFF)
            is_fully_dimmed = True
            touchscreen_device.grab()  # Block the touchscreen

except KeyboardInterrupt:
    print("Script interrupted by user.")
    pass
except Exception as e:
    print(f"An error occurred: {e}")
