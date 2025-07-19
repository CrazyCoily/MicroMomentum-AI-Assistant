from tool_function_registry import register_function

@register_function("show_goals")
def show_goals():
    try:
        with open('goals.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "No goals found."
