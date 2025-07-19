function_registry = {}

def register_function(name):
    def decorator(func):
        function_registry[name.lower()] = func  # store in lowercase for easier matching
        return func
    return decorator

def call_function(name, *args, **kwargs):
    func = function_registry.get(name.lower())
    if func:
        return func(*args, **kwargs)
    return f"❌ Function '{name}' not found."

def get_registered_commands():
    return list(function_registry.keys())
