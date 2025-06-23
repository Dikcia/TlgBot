
import logging
import os
import filetype
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені зображення або документ, і я скажу його тип.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    photo = update.message.photo

    if photo:
        file = await photo[-1].get_file()
    elif document:
        file = await document.get_file()
    else:
        await update.message.reply_text("Надішли фото або документ.")
        return

    file_path = f"temp_{file.file_unique_id}"
    await file.download_to_drive(file_path)

    kind = filetype.guess(file_path)
    if kind:
        file_type = f"{kind.mime} ({kind.extension})"
    else:
        file_type = "Невідомий тип файлу"

    await update.message.reply_text(f"Тип файлу: {file_type}")
    os.remove(file_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    app.run_polling()

if __name__ == "__main__":
    main()
