from datetime import datetime, timedelta

def get_streak():
    try:
        with open("dopamine_log.txt", "r") as f:
            logs = f.readlines()
    except:
        return 0

    if not logs:
        return 0

    streak = 0
    today = datetime.now().date()

    for i in range(0, 7):  # max 7-day streak
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        if any(day_str in log for log in logs):
            streak += 1
        else:
            if i != 0:  # allow missing today's entry
                break

    return streak
