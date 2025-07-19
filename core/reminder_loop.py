import threading
import time
from datetime import datetime
from tool_reminder import check_reminders

def reminder_loop():
    while True:
        check_reminders()
        now = datetime.now()
        seconds_until_next_minute = 60 - now.second
        time.sleep(seconds_until_next_minute)

def start_reminder_loop():
    thread = threading.Thread(target=reminder_loop, daemon=True)
    thread.start()
