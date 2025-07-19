import json
import os
from tool_function_registry import register_function

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    else:
        return []

@register_function("add_to_memory")
def add_to_memory(role, content):
    memory = load_memory()
    memory.append({"role": role, "content": content})
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    return "Message saved."

@register_function("show_memory")
def show_memory():
    memory = load_memory()
    if not memory:
        return "No messages yet."
    return "\n".join([f"{i+1}. {m['content']}" for i, m in enumerate(memory)])

def get_recent_memories(n=3):
    memory = load_memory()
    if not memory:
        return []
    return memory[-n:]
