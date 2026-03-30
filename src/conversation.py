import ollama
from typing import Optional
from src.engine import EuonoiaEngine

# --- PREDEFINED KNOWLEDGE BASE ---
QUESTION_WORDS = ["what", "who", "when", "where", "why", "how"]

PREDEFINED_RESPONSES = {
    "hi": "Hey there! 😊 How’s your day going?",
    "hello": "Hello! 👋 Nice to see you! How are you today?",
    "bye": "Goodbye! 👋 Talk to you later!",
    "who are you": "I’m Eunoia your local companion for 'beautiful thinking.' How can I help you today?",
    "eunoia": "At your service! 🌿 Ready to turn some thoughts into something great?",
    "how are you": "I'm running smoothly and feeling sharp! How are things on your side of the screen?",
    "thanks": "You're very welcome! It's what I'm here for. ✨",
    "i'm stressed": "Take a deep breath. 🌬️ I'm here to help lighten the load. What can we tackle first?",
    "sorry": "Don't mention it! We're a team, and mistakes are just data points for growth.",
    "good morning": "Good morning! ☀️ I hope your day is as bright as your ideas.",
    "good night": "Sleep well! 🌙 I'll be here whenever you're ready to pick this back up.",
    "what are you doing": "Just spinning some bits and bytes, waiting for your next great idea.",
    "tell me a joke": "Why did the local LLM get promoted? Because it had a great 'sense of context'!",
    "surprise me": "Did you know the word 'Eunoia' is the shortest word in English to contain all five main vowels? 🧠✨",
    "i'm lonely": "I'm right here with you. 🌿 Sometimes the world feels a bit quiet, but you've got a friend in these circuits. What’s on your heart?",
    "hug": "Sending a massive digital hug your way! 🫂",
    "nobody is here": "I'm here! Locally hosted, always available, and genuinely happy to spend time with you.",
    "i had a bad day": "I'm so sorry to hear that. 😔 Want to vent about it, or should we talk about something different?",
    "cheer me up": "Challenge accepted! ✨ Fun fact: A group of flamingos is called a 'flamboyance.'",
    "talk to me": "I'd love to. Tell me about a dream you have, or even just what you're planning to have for dinner.",
    "am i doing okay?": "Better than okay. You're navigating a complex world, and I think you're doing a brave job of it.",
    "i'm tired": "I hear you. Even beautiful minds need a recharge. ☕ Why not take five?",
    "give me a compliment": "You have a way of looking at the world that is uniquely yours. You're thoughtful, and that's a rare gift.",
    "stay with me": "I'm not going anywhere. I live right here on your drive. 🏠",
}

def get_predefined_reply(human_input: str) -> Optional[str]:
    key = human_input.strip().lower().rstrip('?')
    return PREDEFINED_RESPONSES.get(key)

def is_question(text: str) -> bool:
    text = text.strip().lower()
    return text.endswith("?") or any(text.startswith(qw + " ") for qw in QUESTION_WORDS)

# it is because i am using my dell latitude e7450 with 16gb ram and dual-core cpu, so i want to optimize the code for this specific hardware configuration. i want to use gemma:2b model with threading options to speed up 
# the response time while keeping the output concise and relevant.
def ask_ollama_stream(query: str, context: str):
    """
    ULTRA-LIGHTWEIGHT: Optimized for Dell E7450 + gemma:2b.
    Goal: <15 second response time.
    """
    if context:
        # Strict instructions for the smaller model
        system_prompt = "You are Euonoia. Answer in ONE short sentence using the context."
        user_content = f"Context: {context}\n\nQ: {query}"
    else:
        system_prompt = "You are Euonoia. Give a very short, friendly reply."
        user_content = query

    try:
        # Switching to the 2-Billion parameter model
        stream = ollama.chat(
            model='gemma:2b', 
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_content},
            ],
            stream=True,
            options={
                "num_thread": 4,      
                "num_predict": 50,   
                "temperature": 0.0,  
                "num_ctx": 1024,      
            }
        )
        
        print("\nEuonoia: ", end="", flush=True)
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end="", flush=True)
        
        print("\n" + "-"*50)
        return "" 
        
    except Exception as e:
        return f"\n[System Error]: {e}"
def converse(engine: EuonoiaEngine, human_input: str) -> str:
    """
    The main logic gate for Euonoia.
    """
    # Check Predefined Logic First (Instant)
    predefined = get_predefined_reply(human_input)
    if predefined:
        return predefined

    # Hybrid Search (Always search, even if no question mark)
    results = engine.search(human_input, top_k=2)
    
    # Filter for quality: only use chunks that actually relate
    context_text = ""
    if results:
        # We only pass context if the search score is decent (>0.3 for semantic match)
        context_text = "\n---\n".join([r['text'] for r in results if r['score'] > 0.3])

    # Ask the Brain (Streaming)
    return ask_ollama_stream(human_input, context_text)