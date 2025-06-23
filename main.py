import os
import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import filetype
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Надішли мені фото або файл, і я визначу його тип.")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document or update.message.photo[-1]
    file_obj = file.get_file()
    file_path = f"temp_{file.file_unique_id}"
    file_obj.download(file_path)

    kind = filetype.guess(file_path)
    if kind:
        file_type = f"{kind.mime} ({kind.extension})"
    else:
        file_type = "Невідомий тип файлу"

    update.message.reply_text(f"Тип файлу: {file_type}")
    os.remove(file_path)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.photo, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
