
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import filetype

def start(update, context):
    update.message.reply_text("Привіт! Надішли мені зображення, і я скажу його тип.")

def handle_photo(update, context):
    photo = update.message.photo[-1]
    file = photo.get_file()
    file_path = "downloaded_image.jpg"
    file.download(file_path)

    kind = filetype.guess(file_path)
    if kind is None:
        update.message.reply_text("Не вдалося визначити тип файлу.")
    else:
        update.message.reply_text(f"Тип файлу: {kind.mime}")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
