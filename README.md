# Raspberry Pi Touchscreen Screensaver
This Python script functions as a screensaver for a touchscreen device. It dims the display after a period of inactivity and wakes it back up upon detecting a touch event.

## Features
- Full Brightness: The display is initially set to full brightness.
- Half-Dim: If no touch events are detected for 10 minutes, the display dims to 50% brightness.
- Full-Dim: If no touch events are detected for 30 minutes, the display is turned off.
- Auto-Wake: The display returns to full brightness upon detecting a touch event.

## Requirements
- Python 3
- evdev library

You can install the required library using apt-get:
```
sudo apt install python3-evdev
```

## Usage
1. Clone the Repository
    ```
    git clone https://github.com/yourusername/touchscreen-screensaver.git
    cd touchscreen-screensaver
    ```
2. Modify the Script
Update the "BRIGHTNESS_FILE" on line 7 and "InputDevice" path one line 32 in the script to match your system configuration.
3. Run the Script
You can run the script manually using:
    ```
    python3 screensaver.py
    ```

## Setting Up as a System Service
To ensure that the screensaver runs automatically at startup, you can set it up as a systemd service.
1. Create a Service file
    ```
    sudo nano /etc/systemd/system/screensaver.service
    ```
2. Add the Following Configuration

   Paste the following configuration into the file (modify the script path to your path):
   ``` screensaver.service
   [Unit]
   Description=Screensaver for touchscreen
   After=multi-user.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/pi/screensaver/screensaver.py
   Restart=on-failure
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and Start the Service

   Enable the service to start on boot:
   ```
   sudo systemctl enable screensaver.service
   ```
   Start the service immediately:
   ```
   sudo systemctl start screensaver.service
   ```
4. Check Service 

   You can check the status of your service with:
   ```
   sudo systemctl status screensaver.service
