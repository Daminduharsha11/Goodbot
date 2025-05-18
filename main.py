
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text('Hello! I am your bot.')

async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("Please set the TELEGRAM_TOKEN environment variable")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
