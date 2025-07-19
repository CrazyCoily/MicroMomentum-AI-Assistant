import random

from tool_function_registry import register_function

@register_function("get_reflection_prompt")
def get_reflection_prompt():
    prompts = [
        "What emotion did I feel most today?",
        "What triggered a dopamine spiral today?",
        "What am I proud of from the past 24 hours?",
        "Where did I avoid discomfort today?",
        "What’s 1 thing I can improve tomorrow?"
    ]
    return random.choice(prompts)
