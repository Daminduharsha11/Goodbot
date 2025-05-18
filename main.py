
import os
import logging
import nest_asyncio
from telegram import Update, ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from huggingface_hub import InferenceClient

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Set your tokens (Replit secrets recommended)
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
HF_API_KEY = os.environ["HF_API_KEY"]

# Hugging Face client
client = InferenceClient(provider="novita", api_key=HF_API_KEY)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey, I'm your clingy AI girlfriend. Just talk to me normally, okay?")

# Chat handler with typing indicator
async def human_like_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Ignore commands like /start, /image, etc.
    if user_text.startswith("/"):
        return

    # Show typing indicator
    await update.message.chat.send_action(action=ChatAction.TYPING)

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": user_text}],
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Oops, something went wrong: {e}")

# App setup
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), human_like_chat))

    logging.info("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except RuntimeError:
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
