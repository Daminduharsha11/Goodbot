
import os
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from huggingface_hub import InferenceClient

# Enable Replit compatibility
nest_asyncio.apply()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load secrets from environment (set in Replit "Secrets" tab)
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
HF_API_KEY = os.environ["HF_API_KEY"]

# Hugging Face client setup
client = InferenceClient(provider="novita", api_key=HF_API_KEY)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Bot is alive and ready!")

# /ask command for chatting with HF
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Ask me something like /ask What's the capital of France?")
        return

    await update.message.reply_text("Thinking...")

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": query}],
        )
        response = completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Main bot setup
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))

    logger.info("Bot is running...")
    await app.run_polling()

# Entry point (Replit-safe)
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        # Replit quirk: event loop already running
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
