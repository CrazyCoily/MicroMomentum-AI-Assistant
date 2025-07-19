import json
import os
import datetime
import subprocess
import sys

def classify_event_with_ai(message: str) -> str:
    """
    Uses a local LLM (via Ollama) to classify whether the activity is good or bad
    based on its long-term impact on discipline and focus.
    """
    prompt = f"Classify this activity as 'good' or 'bad' based on whether it supports long-term discipline and focus:\n\nActivity: {message}\n\nAnswer with only 'good' or 'bad'."
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
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

def log_event(message: str):
    """
    Logs the activity message with AI classification and timestamp to a JSON file.
    """
    log_file = "dopamine_log.json"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ai_tag = classify_event_with_ai(message)

    entry = {
        "timestamp": now,
        "message": message,
        "ai_tag": ai_tag
    }

    # Load existing log or create new one
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"[LOGGED] {message} ({ai_tag}) at {now}")

def log_dopamine_event(message: str):
    """
    Function interface for main.py to log a dopamine event with AI tagging.
    """
    log_event(message)

def test_classifier():
    """
    Test the AI classifier on sample inputs.
    """
    test_messages = [
        "Scrolled TikTok for 2 hours",
        "Studied machine learning for 45 minutes",
        "Watched YouTube while eating",
        "Took a 10-minute walk outside"
    ]
    for msg in test_messages:
        tag = classify_event_with_ai(msg)
        print(f"{msg} -> {tag}")

# CLI Support
if __name__ == "__main__":
    if "--test" in sys.argv:
        test_classifier()
    elif len(sys.argv) > 1:
        input_message = " ".join(sys.argv[1:])
        log_event(input_message)
    else:
        print("Usage:")
        print(" python tool_log_dopamine_event.py <your activity>")
        print(" python tool_log_dopamine_event.py --test")
