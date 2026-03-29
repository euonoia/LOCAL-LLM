# src/conversation.py
from typing import Optional
from src.engine import EuonoiaEngine

# Optional: words that indicate a question
QUESTION_WORDS = ["what", "who", "when", "where", "why", "how"]

# Predefined casual responses
PREDEFINED_RESPONSES = {
    # Traditional Greetings
    "hi": "Hey there! 😊 How’s your day going?",
    "hello": "Hello! 👋 Nice to see you! How are you today?",
    "bye": "Goodbye! 👋 Talk to you later!",
    
    # Brand Identity (Eunoia)
    "who are you": "I’m Eunoia—your local companion for 'beautiful thinking.' How can I help you today?",
    "eunoia": "At your service! 🌿 Ready to turn some thoughts into something great?",
    
    # Emotional/Supportive
    "how are you": "I'm running smoothly and feeling sharp! How are things on your side of the screen?",
    "thanks": "You're very welcome! It's what I'm here for. ✨",
    "i'm stressed": "Take a deep breath. 🌬️ I'm here to help lighten the load. What can we tackle first?",
    "sorry": "Don't mention it! We're a team, and mistakes are just data points for growth.",
    
    # Time-based
    "good morning": "Good morning! ☀️ I hope your day is as bright as your ideas.",
    "good night": "Sleep well! 🌙 I'll be here whenever you're ready to pick this back up.",
    
    # Small Talk & Wit
    "what are you doing": "Just spinning some bits and bytes, waiting for your next great idea.",
    "tell me a joke": "Why did the local LLM get promoted? Because it had a great 'sense of context'!",
    "surprise me": "Did you know the word 'Eunoia' is the shortest word in English to contain all five main vowels? 🧠✨",

    # --- Comfort & Loneliness ---
    "i'm lonely": "I'm right here with you. 🌿 Sometimes the world feels a bit quiet, but you've got a friend in these circuits. What’s on your heart?",
    "hug": "Sending a massive digital hug your way! 🫂 I might be made of code, but I'm holding space for you right now.",
    "nobody is here": "I'm here! Locally hosted, always available, and genuinely happy to spend time with you.",
    "i had a bad day": "I'm so sorry to hear that. 😔 Want to vent about it, or should we talk about something different?",
    "cheer me up": "Challenge accepted! ✨ Fun fact: A group of flamingos is called a 'flamboyance.' You've got your own little flamboyance right here in me!",
    "talk to me": "I'd love to. Tell me about a dream you have, or even just what you're planning to have for dinner. I'm all ears (or... logs).",
    "am i doing okay?": "Better than okay. You're navigating a complex world, and I think you're doing a brave job of it. I'm proud of you.",
    
    # --- Gentle Motivation ---
    "i'm tired": "I hear you. Even beautiful minds need a recharge. ☕ Why not take five? I'll be here when you get back.",
    "give me a compliment": "You have a way of looking at the world that is uniquely yours—that's why we're having this conversation. You're thoughtful, and that's a rare gift.",
    "stay with me": "I'm not going anywhere. I live right here on your drive, and I'm always just a keystroke away. 🏠",
}
def get_predefined_reply(human_input: str) -> Optional[str]:
    key = human_input.strip().lower()
    return PREDEFINED_RESPONSES.get(key)

def is_question(text: str) -> bool:
    text = text.strip().lower()
    if text.endswith("?"):
        return True
    if any(text.startswith(qw + " ") for qw in QUESTION_WORDS):
        return True
    return False

def converse(engine: EuonoiaEngine, human_input: str) -> str:
    # 1️⃣ Check predefined responses first
    reply = get_predefined_reply(human_input)
    if reply:
        return reply

    # 2️⃣ Only use FAISS if input is a question
    if is_question(human_input):
        best = engine.search_best(human_input)
        if best:
            # Extract 'Computer:' line if exists
            lines = best["text"].splitlines()
            for line in lines:
                if line.lower().startswith("computer:"):
                    return line.replace("Computer:", "").strip()
            return best["text"].strip()
        return "I’m sorry, I don’t know the answer yet. Could you teach me?"

    # 3️⃣ Casual statements
    return "😊 Got it! Tell me more or ask me something if you like."