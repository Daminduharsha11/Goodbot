
import random

# Some predefined responses for variety
GREETINGS = [
    "Hello! How can I help you today?",
    "Hi there! What's on your mind?",
    "Greetings! How may I assist you?",
]

FAREWELLS = [
    "Goodbye! Take care!",
    "See you later!",
    "Bye! Have a great day!",
]

DEFAULT_RESPONSES = [
    "That's interesting! Tell me more.",
    "I understand. Please continue.",
    "I see what you mean.",
    "Hmm, that's a good point.",
]

async def generate_response(message: str) -> str:
    """Generate a response based on the input message."""
    message = message.lower().strip()
    
    # Basic response logic
    if any(word in message for word in ['hello', 'hi', 'hey']):
        return random.choice(GREETINGS)
    
    if any(word in message for word in ['bye', 'goodbye', 'see you']):
        return random.choice(FAREWELLS)
    
    if '?' in message:
        return "That's an interesting question! Let me think about it..."
    
    # Default response if no specific condition is met
    return random.choice(DEFAULT_RESPONSES)
