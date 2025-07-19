import json
import os

PROFILE_FILE = "profile.json"

default_profile = {
    "name": "Your Name",
    "focus": "Self-improve",
    "level": "New"
}

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    else:
        save_profile(default_profile)
        return default_profile

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)

def show_profile():
    profile = load_profile()
    return f"""
🧠 Profile Overview
Name   : {profile['name']}
Focus  : {profile['focus']}
Level  : {profile['level']}
"""

def update_profile(key, value):
    profile = load_profile()
    if key in profile:
        profile[key] = value
        save_profile(profile)
        return f"✅ Updated {key} to: {value}"
    else:
        return "⚠️ Invalid profile key. Use: name, focus, or level."
