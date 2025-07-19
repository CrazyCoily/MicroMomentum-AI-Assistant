import subprocess
import json
import sys
from datetime import datetime

LOG_FILE = "dopamine_log.json"

def classify_event_with_ai(message: str) -> str:
    try:
        prompt = (
            f"Classify the following activity as either 'good' or 'bad' for long-term focus and discipline. "
            f"Respond with only one word: good or bad.\n\nActivity: {message}"
        )

        command = ["ollama", "run", "llama3", prompt]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)

        output = result.stdout.strip().lower()
        first_word = output.split()[0]

        if first_word in ["good", "bad"]:
            return first_word
        else:
            print(f"[WARN] Unexpected AI output: {output}")
            return "unknown"

    except Exception as e:
        print(f"[ERROR] AI classification failed: {e}")
        return "unknown"

def log_event(message: str):
    original_message = message.strip()

    # Manual override
    if "!good" in original_message:
        classification = "good"
        message = original_message.replace("!good", "").strip()
    elif "!bad" in original_message:
        classification = "bad"
        message = original_message.replace("!bad", "").strip()
    else:
        classification = classify_event_with_ai(original_message)
        message = original_message

    entry = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "classification": classification
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"✅ Logged: {message} | Tag: {classification}")
    except Exception as e:
        print(f"[ERROR] Failed to write to log: {e}")

def test_classifier():
    test_cases = [
        "worked out in the morning",
        "watched TikTok for an hour",
        "coded my AI assistant",
        "scrolled Reddit before sleep",
        "studied chemistry",
        "ate chips and soda late at night"
    ]
    for case in test_cases:
        tag = classify_event_with_ai(case)
        print(f"{case} => {tag}")

if __name__ == "__main__":
    if "--test" in sys.argv:
        test_classifier()
    elif len(sys.argv) > 1:
        input_message = " ".join(sys.argv[1:])
        log_event(input_message)
    else:
        print("Usage:\n  python log_dopamine_event.py <your activity>\n  python log_dopamine_event.py --test")
