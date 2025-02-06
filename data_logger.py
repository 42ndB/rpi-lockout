# -*- coding: utf-8 -*-
'''
  # demo_get_distance_with_button.py
  #
  # Connect board with Raspberry Pi and a button.
  # Run this demo to log distance and button state to a CSV file.
  #
  # Connect A01 to UART, and button to GPIO.
  # Logs distance and button state with timestamps.
  #
  # Copyright   [DFRobot](http://www.dfrobot.com), 2016
  # Copyright   GNU Lesser General Public License
  #
  # version  V1.3
  # date  2025-02-05
'''

import time
import csv
import RPi.GPIO as GPIO
from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board

# Initialize the sensor
board = Board()

# Button GPIO setup
BUTTON_PIN = 4  # Change to your button's GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Adjust to PUD_DOWN if necessary

# Function to print and log distance and button state
def print_and_log_data(dis, pressed, timestamp):
    if board.last_operate_status == board.STA_OK:
        print(f"Timestamp: {timestamp:.3f} s, Distance: {dis} mm, Button Pressed: {pressed}")
        return dis, pressed
    elif board.last_operate_status == board.STA_ERR_CHECKSUM:
        print("ERROR: Checksum failed!")
    elif board.last_operate_status == board.STA_ERR_SERIAL:
        print("ERROR: Serial open failed!")
    elif board.last_operate_status == board.STA_ERR_CHECK_OUT_LIMIT:
        print(f"ERROR: Above the upper limit: {dis}")
    elif board.last_operate_status == board.STA_ERR_CHECK_LOW_LIMIT:
        print(f"ERROR: Below the lower limit: {dis}")
    elif board.last_operate_status == board.STA_ERR_DATA:
        print("ERROR: No data!")
    return None, None

if __name__ == "__main__":
    # File setup
    filename = "distance_button_data.csv"
    
    # Set distance range
    dis_min = 0   # Minimum ranging threshold: 0mm
    dis_max = 7500 # Maximum ranging threshold: 7500mm
    board.set_dis_range(dis_min, dis_max)
    
    # Write header to CSV file
    with open(filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp (seconds)", "Distance (mm)", "Button Pressed"])
    
    print("Recording distance and button data. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Get current timestamp
            timestamp = time.time()  # Current time in seconds (float)
            
            # Get distance
            distance = board.getDistance()
            
            # Check button state
            pressed = not GPIO.input(BUTTON_PIN)  # True if button is pressed
            
            # Log distance and button state if valid
            logged_distance, logged_pressed = print_and_log_data(distance, pressed, timestamp)
            if logged_distance is not None:
                with open(filename, mode='a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([f"{timestamp:.3f}", logged_distance, logged_pressed])  # Log timestamp to milliseconds
            
            # Delay for stability
            time.sleep(0.3)  # Delay time < 0.6s
    except KeyboardInterrupt:
        print("\nRecording stopped. Data saved to", filename)
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
