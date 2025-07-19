from datetime import datetime

def summarize_day():
    try:
        with open("dopamine_log.txt", "r") as f:
            logs = f.readlines()
    except:
        return "📭 No dopamine events found."

    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [line for line in logs if line.startswith(f"[{today}")]

    if not today_logs:
        return "🕳️ You haven't logged any wins today yet."

    return "\n📅 Today’s Wins:\n" + "".join(today_logs)
