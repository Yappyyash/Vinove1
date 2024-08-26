from pynput import mouse, keyboard
from PIL import ImageGrab
import datetime
import threading
import time
import os
import sys
import subprocess
import platform
# Global variables to track activity
last_active_time = None
active_time_seconds = 0
movement_count = 0
active_time_calculated = False  # Flag to ensure active time is only calculated once per interval
finaldata = []
key_count=0
mouse_count =0
# Define thresholds
IDLE_THRESHOLD_SECONDS = 60  # Time in seconds after which the user is considered idle
WORK_THRESHOLD_MOVEMENTS = 60  # Minimum movements to consider it genuine work

activity_data = {
    'status': '',
    'active_time': 0,
    'screenshot_path': '', 
    'finaldata':[], 
    'mousecount':0,
    'keycount':0
}

# Function to track mouse movements
def on_move(x, y):
    global movement_count
    movement_count += 1
    update_activity()

def on_click(x, y, button, pressed):
    global movement_count
    global mouse_count
    if pressed:
        movement_count += 1
        mouse_count+=1
        activity_data['mousecount']=mouse_count
        update_activity()

def on_scroll(x, y, dx, dy):
    global movement_count
    movement_count += 1
    update_activity()

# Function to track keyboard events
def on_press(key):
    global movement_count
    global key_count
    movement_count += 1
    key_count+=1
    activity_data['keycount']=key_count
    update_activity()

# Function to update user activity
def update_activity():
    global last_active_time, active_time_seconds, active_time_calculated
    current_time = datetime.datetime.now()
    if last_active_time is not None:
        idle_time = (current_time - last_active_time).total_seconds()
        if idle_time < IDLE_THRESHOLD_SECONDS:
            active_time_seconds += idle_time
    last_active_time = current_time
    active_time_calculated = False  # Reset the flag whenever there's user activity

# Function to analyze activity
def analyze_activity():
    global activity_data, movement_count, active_time_calculated, finaldata
    data = []
    if not active_time_calculated:  # Only calculate active time if it hasn't been done yet
        if movement_count >= WORK_THRESHOLD_MOVEMENTS:
            activity_data['status'] = 'User activity is genuine.'
        else:
            activity_data['status'] = 'User appears idle or non-genuine.'
        data.append(active_time_seconds)
        active_time_in_minutes = round(data[0] / 60, 2)  # Convert seconds to minutes
        activity_data['active_time'] = active_time_in_minutes
        finaldata.append(active_time_in_minutes)  # Store the activity time in the finaldata list
        activity_data['finaldata'] = finaldata  # Update the activity_data with the finaldata list
        data.clear()
        active_time_calculated = True  # Set the flag to avoid recalculating in the same interval

    print(f"Status: {activity_data['status']}")
    print(f"Active Time: {activity_data['active_time']} minutes")
    print(f"Final Data: {activity_data['finaldata']}")
# Function to capture a screenshot and update the path
def capture_screenshot(save_path='media/screenshot'):
    global activity_data
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = ImageGrab.grab()
    screenshot_path = f'{save_path}_{timestamp}.png'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    screenshot.save(screenshot_path, quality=85)
    pic_save = 'C:/Users/UNITECH/Desktop/Vinove/vinove/' + screenshot_path
    activity_data['screenshot_path'] = pic_save
    print(f"Screenshot saved to {screenshot_path}")

# Function to periodically analyze activity and capture screenshots
def periodic_analysis(interval=1800):
    global movement_count, active_time_seconds, last_active_time, active_time_calculated
    while True:
        analyze_activity()
        capture_screenshot()
        
        # Reset counters for the next interval
        movement_count = 0
        last_active_time = None
        active_time_seconds = 0
        active_time_calculated = False  # Reset flag for the next interval

        time.sleep(interval)

# Function to start the mouse and keyboard listeners
def start_listeners():
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, \
         keyboard.Listener(on_press=on_press) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

# Start the listeners in a separate thread

listeners_thread = threading.Thread(target=start_listeners, daemon=True)
print("Activity tracking started")
listeners_thread.start()
# Start the periodic activity analysis in a separate thread
analysis_thread = threading.Thread(target=periodic_analysis, args=(120,), daemon=True)
analysis_thread.start()
finaldata.pop(0)
