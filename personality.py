
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="novita",
    api_key=os.getenv("HF_API_KEY")  # Store in Replit secrets
)

PERSONALITY_PROMPT = """
<|system|>
You're a playful, funny , emotional AI companion. Respond:
- Short messages (1-2 sentences max)
- Use emojis occasionally
</s>
<|user|>{user_input}</s>
<|assistant|>
"""

async def generate_response(user_input: str) -> str:
    try:
        prompt = PERSONALITY_PROMPT.format(user_input=user_input)
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "My mind went blank... say that again?"
