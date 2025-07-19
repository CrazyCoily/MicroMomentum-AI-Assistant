from tool_function_registry import register_function

@register_function("set_goal")
def set_goal(goal):
    with open("goals.txt", "a") as f:
        f.write(goal + "\n")
    return f"[✅] Goal set: {goal}"
