# tool_proactive_prompt.py

import random

def get_proactive_prompt():
    prompts = [
        "💡 Want to log a small win from today?",
        "🎯 Set a mini goal to stay focused?",
        "🧠 Need a mental clarity prompt?",
        "📌 How do you feel right now? I’ll help you log it.",
        "🔁 Restart momentum with a reflection prompt?"
    ]
    return random.choice(prompts)
