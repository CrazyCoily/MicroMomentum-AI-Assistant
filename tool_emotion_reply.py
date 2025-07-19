import ollama

def generate_emotional_reply(func_name, arg=None):
    try:
        prompt = f"""
You're the voice of a productivity assistant. Speak with warmth, motivation, and human tone.

This just happened:
🧠 Function: {func_name}
📦 Data: {arg or 'none'}

Respond in a single short sentence, like:
- "✅ Goal saved. Let’s make it happen."
- "🎉 Logged it! Great work."
- "🧠 Memory updated. You're building momentum."

Be friendly and emotional, but concise.
"""

        response = ollama.chat(
            model="llama3",  # or whatever you’re using
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"⚠️ Emotion engine failed: {e}"
