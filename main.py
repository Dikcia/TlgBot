
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import filetype

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені зображення, і я скажу його тип.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_path = "/tmp/downloaded_image"
    await file.download_to_drive(file_path)

    kind = filetype.guess(file_path)
    if kind is None:
        await update.message.reply_text("Не вдалося визначити тип файлу.")
    else:
        await update.message.reply_text(f"Тип файлу: {kind.mime}")

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_file))

    app.run_polling()
