import json
from datetime import datetime
from tool_function_registry import register_function

REMINDER_FILE = "reminders.json"

def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=2)

@register_function("add_reminder")
def add_reminder(arg):
    try:
        time_str, *message = arg.strip().split(" ")
        msg = " ".join(message)
        datetime.strptime(time_str, "%H:%M")  # validate time format

        data = load_reminders()
        data.append({
            "time": time_str,
            "message": msg
        })
        save_reminders(data)

        return f"⏰ Reminder set for {time_str}: {msg}"
    except:
        return "❌ Usage: /remind HH:MM your message"

def check_reminders():
    now = datetime.now().strftime("%H:%M")
    reminders = load_reminders()
    for r in reminders:
        if r["time"] == now:
            print("\n" + "🟡" * 40)
            print(f"🔔 REMINDER @ {r['time']}: {r['message']}")
            print("🟡" * 40 + "\n")

