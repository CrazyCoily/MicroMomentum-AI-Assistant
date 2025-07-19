from tool_function_registry import register_function
from datetime import datetime
import json
import os
import subprocess

# Log file path
LOG_FILE = "dopamine_log.json"
print(f"[DEBUG] Logging to: {LOG_FILE}")
print(f"[DEBUG] Current working directory: {os.getcwd()}")

def get_timestamp():
    return datetime.now().isoformat()

def classify_event_with_ai(message: str) -> str:
    """
    Use Ollama + local LLM to classify a behavior log as good or bad,
    considering intent, time, and discipline impact.
    """
    prompt = f"""
Classify the following activity as either 'good' or 'bad' for long-term focus, discipline, and mental well-being.

Take into account:
- The nature of the activity (productive vs indulgent)
- The intent behind it (reward vs avoidance)
- Its impact on long-term goals

Activity: '{message}'

Reply with only one word: 'good' or 'bad'.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip().lower()
        if "good" in output:
            return "good"
        elif "bad" in output:
            return "bad"
        else:
            return "unknown"
    except Exception as e:
        print(f"[ERROR] AI classification failed: {e}")
        return "unknown"


@register_function("log_dopamine_event")
def log_dopamine_event(message):
    print(f"[DEBUG] log_dopamine_event CALLED with: {message}")

    if not message:
        return "❌ No message provided."

    # Classify using AI
    classification = classify_event_with_ai(message)
    if classification == "unknown":
        return "❌ AI couldn't classify the message."

    # Load existing logs
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        except json.JSONDecodeError:
            print("[WARN] Corrupted log file. Starting fresh.")
            log = []
    else:
        log = []

    # Append new entry
    entry = {
        "timestamp": get_timestamp(),
        "type": classification,
        "message": message,
        "classified_by": "AI"
    }
    log.append(entry)

    # Save back to file
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        print(f"[✅] JSON written to: {LOG_FILE}")
        print(f"[📝] Entry:\n{json.dumps(entry, indent=2)}")
    except Exception as e:
        print(f"[ERROR] Failed to write log: {e}")
        return "❌ Failed to save log."

    return f"✅ Logged: [{entry['type'].upper()}] {entry['message']} at {entry['timestamp']}"
