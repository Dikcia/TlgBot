import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Виводимо все в лог
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # DEBUG замість INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Команда /start отримана")
    await update.message.reply_text("Привіт! Я бот і працюю на PTB 20+ ✅")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN не встановлено!")
    else:
        logging.info("Запускаємо бота…")
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling()
