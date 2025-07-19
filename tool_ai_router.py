import re
import json
import ollama

def determine_function(user_input):
    system_prompt = """
You are a strict function router for a productivity assistant. 
Your job is to read the user's input and decide which internal function to call.

🧠 Important Rules:
- You MUST only return a JSON object.
- NEVER include markdown, explanations, or extra text. Just the JSON.
- If the input is unclear, return: {"function": null, "arg": null}
- NEVER prefix the response with anything like "Output:" or "Here is the result:"
- Available Functions:
  - log_dopamine_event (arg): For anything that represents a small win, progress, or a positive/negative habit.
    Format: "type message"
    Where 'type' can be:
      - "achievement": finished a task or goal
      - "craving": gave in to a bad habit (e.g., binged TikTok, ate junk food)
      - "resisted": successfully avoided a bad habit (e.g., closed TikTok, skipped junk food)
      - "failure": skipped something important or gave up on a goal
  - set_goal (arg)
  - show_goals
  - clear_goals
  - get_reflection_prompt
  - summarize_day
  - add_to_memory (arg)
  - show_memory

💡 Examples:
User: "Just finished my workout"  
→ {"function": "log_dopamine_event", "arg": "achievement finished my workout"}

User: "Binged YouTube for 3 hours"  
→ {"function": "log_dopamine_event", "arg": "craving binged YouTube for 3 hours"}

User: "Just stopped scrolling TikTok"  
→ {"function": "log_dopamine_event", "arg": "resisted just stopped scrolling TikTok"}

User: "Skipped gym again..."  
→ {"function": "log_dopamine_event", "arg": "failure skipped gym again"}
"""

    response = ollama.chat(
        model="llama3",  # switch to llama3 when finished
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    raw_output = response['message']['content']
    # print("🧠 Raw LLM Output:", raw_output) # debug check

    # Try to extract the first JSON object using regex
    match = re.search(r'\{.*?\}', raw_output, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group())
            return result.get("function"), result.get("arg")
        except json.JSONDecodeError:
            print("❌ JSON decode failed.")
    else:
        print("⚠️ No JSON found in LLM response.")

    return None, None
