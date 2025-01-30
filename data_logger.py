# ‐*‐ coding:utf‐8 ‐*‐ 
'''
  # demo_get_distance.py
  #
  # Connect board with raspberryPi.
  # Run this demo.
  #
  # Connect A01 to UART
  # Get the distance value and log to a CSV file with timestamps
  #
  # Copyright   [DFRobot](http://www.dfrobot.com), 2016
  # Copyright   GNU Lesser General Public License
  #
  # version  V1.1
  # date  2025-01-16
'''
import time
import csv
from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board

# Initialize the sensor
board = Board()

# Function to print and return the distance
def print_and_log_distance(dis):
    if board.last_operate_status == board.STA_OK:
        print(f"Distance: {dis} mm")
        return dis
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
    return None

if __name__ == "__main__":
    # File setup
    filename = "distance_data.csv"
    
    # Set distance range
    dis_min = 0   # Minimum ranging threshold: 0mm
    dis_max = 7500 # Maximum ranging threshold: 7500mm
    board.set_dis_range(dis_min, dis_max)
    
    # Write header to CSV file
    with open(filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Distance (mm)"])
    
    print("Recording distance data. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Get distance
            distance = board.getDistance()
            
            # Log distance if valid
            logged_distance = print_and_log_distance(distance)
            if logged_distance is not None:
                with open(filename, mode='a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), logged_distance])
            
            # Delay for stability
            time.sleep(0.3)  # Delay time < 0.6s
    except KeyboardInterrupt:
        print("\nRecording stopped. Data saved to", filename)
