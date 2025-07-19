from tool_function_registry import function_registry, call_function

def determine_manual_command(user_input):
    lowered_input = user_input.lower().strip()
    print(f"[DEBUG] Registered commands: {list(function_registry.keys())}")
    print(f"[DEBUG] User input: '{lowered_input}'")

    for command in function_registry:
        if lowered_input.startswith(command.replace("_", " ")):
            arg = user_input[len(command):].strip()
            return command, arg


    return None, None


def route_command(user_input):
    command, arg = determine_manual_command(user_input)
    if command:
        try:
            result = call_function(command, arg) if arg else call_function(command)
            return result
        except Exception as e:
            return f"[❌] Error in command '{command}': {e}"
    else:
        return "🤔 Unknown command. Type `/help` or check spelling."
