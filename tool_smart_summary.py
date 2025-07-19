import ollama
from datetime import datetime


def ask_llm(prompt):
    response = ollama.chat(
        model='llama3',
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

from tool_function_registry import register_function

@register_function("summarize_day")
def summarize_day():
    try:
        with open('dopamine_log.txt', 'r') as f:
            dopamine = f.read()
    except FileNotFoundError:
        dopamine = "No dopamine log."

    try:
        with open('goals.txt', 'r') as f:
            goals = f.read()
    except FileNotFoundError:
        goals = "No goals logged."

    full_prompt = f"""
Today’s dopamine log:
{dopamine}

Today’s goals:
{goals}

Based on this, summarize my day and give 3 brutally honest suggestions to improve tomorrow.
"""
    return ask_llm(full_prompt)