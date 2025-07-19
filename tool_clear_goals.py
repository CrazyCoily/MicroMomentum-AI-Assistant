from tool_function_registry import register_function

@register_function("clear_goals")
def clear_goals():
    open('goals.txt', 'w').close()
    return "Goals cleared."
