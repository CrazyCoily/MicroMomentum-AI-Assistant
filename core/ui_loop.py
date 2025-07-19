import json
import re
from datetime import datetime
from core.command_router import determine_manual_command
from tool_log_dopamine_event import log_dopamine_event
from tool_set_goal import set_goal
from tool_show_goals import show_goals
from tool_clear_goals import clear_goals
from tool_reflection_prompt import get_reflection_prompt
from tool_smart_summary import summarize_day as smart_summarize
from tool_memory import add_to_memory, show_memory, get_recent_memories
from tool_proactive_prompt import get_proactive_prompt
from tool_emotion_reply import generate_emotional_reply
from tool_log_viewer import summarize_day as log_summarize
from tool_profile import show_profile, update_profile
from tool_streak import get_streak
from tool_log_mood import log_mood
from tool_reminder import add_reminder, load_reminders
from tool_function_registry import call_function
from tool_ai_router import determine_function as llm_router



def run_ui():
    print("\n👋 Welcome to MicroMomentum.")
    print("\n🧠 Loading your memory...")

    recent = get_recent_memories()
    if recent:
        for mem in recent:
            print(f"📌 {mem['content']}")
    else:
        print("🕳️ No memories stored yet. Let’s start logging what matters.\n")

    print("Type '/help' to see available commands. Type 'exit' to quit. Type '/reset' to reset all logged memories.")
    print("🟰" * 40)

    while True:
        user_input = input("🔍 Your request: ").strip()

        if user_input.lower() in ["/exit", "exit", "quit"]:
            print("👋 Exiting. Show up tomorrow — momentum compounds.")
            break

        if user_input.lower() in ["/help", "help", "?"]:
            show_help()
            continue

        if user_input.lower() == "/reset":
            open("memory.json", "w").write("[]")
            open("goals.json", "w").write("[]")
            print("🔄 Memory and goals reset.")
            continue

        if user_input.lower().startswith("/log win"):
            msg = user_input[len("/log win"):].strip()
            if msg:
                log_dopamine_event("win", msg)
                print(f"💥 Win logged: {msg}")
            else:
                print("⚠️ Usage: /log win [your win message]")
            continue

        if user_input.lower().startswith("/log mood"):
            try:
                _, _, mood_value = user_input.split(" ")
                print(log_mood(mood_value))
            except:
                print("❌ Usage: /log mood [1-5]")
            continue

        if user_input.lower() == "/status":
            get_status()
            print(f"🔥 Current streak: {get_streak()} days")
            continue

        if user_input.lower() == "/why":
            show_why()
            continue

        if user_input.lower() == "/daily":
            print(smart_summarize())
            continue

        if user_input.lower().startswith("/remind"):
            msg = user_input[len("/remind"):].strip()
            print(add_reminder(msg))
            continue

        if user_input.lower() == "/show reminders":
            reminders = load_reminders()
            if reminders:
                for r in reminders:
                    print(f"🕒 {r['time']} → {r['message']}")
            else:
                print("📭 No reminders set.")
            continue

        func_name, arg = determine_manual_command(user_input)  # manual /commands
        if func_name is None:
            func_name, arg = llm_router(user_input)  # fallback to LLM

        if func_name:
            print(f"[DEBUG] Routed to: {func_name} | arg: {arg}")
            try:
                result = call_function(func_name, arg) if arg else call_function(func_name)
                print(result)
            except Exception as e:
                print(f"❌ Error while calling '{func_name}': {e}")
            continue


        if func_name is None:
            def looks_like_gibberish(text):
                # If it's mostly numbers/symbols or a random string, return True
                return bool(re.match(r"^[^a-zA-Z\s]{5,}$", text.strip()))

            if looks_like_gibberish(user_input):
                print("🤔 Hmm, I didn't understand that.")
                print("🧠 Try something like 'show goals' or type /help.")
            else:
                # If input seems human, show emotional response
                emotional = generate_emotional_reply(user_input)
                if emotional:
                    print(emotional)

            print(get_proactive_prompt())
            continue


    try:
        result = call_function(func_name, arg) if arg else call_function(func_name)

        if "❌" in str(result):
            print(result)
        else:
            if func_name == "set_goal":
                print(f"🎯 Got it. I'll keep you focused on: {arg}")
            elif func_name == "log_dopamine_event":
                print(f"💪 Nice! Logged: {arg}. You earned it.")
            elif func_name == "get_reflection_prompt":
                print(f"🧘 Here's something to think about:\n{result}")
            else:
                print(result)

    except Exception as e:
        print(f"❌ Error while calling '{func_name}': {e}")


    except Exception as e:
        print(f"❌ Error while calling '{func_name}': {e}")


def show_help():
    print("\n📘 MicroMomentum Commands:")
    print("  /help               → Show this menu")
    print("  /exit               → Quit the assistant")
    print("  /show goals         → List all current goals")
    print("  /clear goals        → Remove all goals")
    print("  /add memory [text]  → Save a memory")
    print("  /show memory        → Show stored memories")
    print("  /reflect            → Get a reflection question")
    print("  /summarize          → Summarize today")
    print("  /reset              → Reset memory + goals\n")
    print("  /log win [msg]      → Quick log a win (e.g. /log win finished 10 pages)")
    print("  /daily              → Show today’s dopamine log summary")
    print("  /profile            → Show your builder identity")
    print("  /update profile ... → Update your profile info (e.g., update profile name 'Your name goes here')")
    print("  /log mood [1-10]    → Track your mood today (1 = low, 10 = best)")


def get_status():
    try:
        with open("goals.json", "r") as f:
            goals = json.load(f)
    except:
        goals = []

    try:
        with open("memory.json", "r") as f:
            memories = json.load(f)
    except:
        memories = []

    try:
        with open("dopamine_log.txt", "r") as f:
            lines = f.readlines()
            last = lines[-1].strip() if lines else "None yet"
    except:
        last = "None yet"

    if last != "None yet":
        try:
            ts_str = last.split("]")[0].strip("[")
            last_time = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            delta = datetime.now() - last_time
            hours_ago = round(delta.total_seconds() / 3600, 1)
        except:
            hours_ago = "?"
    else:
        hours_ago = "?"

    if goals or memories or last != "None yet":
        print("\n📊 Status Report:")
        print(f"🧠 Memories logged: {len(memories)}")
        print(f"🎯 Goals set: {len(goals)}")
        print(f"💪 Last dopamine event: {last} ({hours_ago} hours ago)\n")
    else:
        print("\n🕳️ No status found. You haven’t started yet.\n")


def show_why():
    print("\n🌌 Why I'm Building MicroMomentum:")
    print("To escape mediocrity, build AI tools, control my time, and create something timeless.\n")
