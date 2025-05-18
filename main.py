
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from personality import generate_response  # Our AI module

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        response = await generate_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Oops! I'm feeling dizzy... Try again later~")

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Missing TELEGRAM_TOKEN")
    
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
