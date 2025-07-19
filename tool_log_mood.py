import json
from datetime import datetime
from tool_function_registry import register_function

MOOD_FILE = "mood_log.json"

@register_function("log_mood")
def log_mood(mood_level):
    try:
        mood = int(mood_level)
        if mood < 1 or mood > 5:
            return "⚠️ Please enter a mood between 1 (lowest) and 5 (best)."
    except:
        return "❌ Invalid input. Try: log mood 3"

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood
    }

    try:
        with open(MOOD_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(entry)

    with open(MOOD_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    return f"🧠 Mood logged: {mood}/5"
