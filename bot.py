import requests
from io import BytesIO
from PIL import Image
import pytesseract
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7912505187:AAFyp71VkSWXh0KElcK4oG73McmZj231ODE"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to FakeCure AI!\n\nSend me any health-related message or a screenshot, and I’ll check if it’s fake or not, and give you the correct info!"
    )

# Handle plain text
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = requests.post("http://127.0.0.1:5000/text-check", json={"text": user_message}, timeout=5)
        result = response.json()
        status = result.get("status", "Unknown")
        suggestion = result.get("suggestion", "No suggestion found.")
        source = result.get("source", None)
        reply = f"{status}\n\n{suggestion}"
        if source:
            reply += f"\n\n🔗 Source: {source}"
        
        await update.message.reply_text(f"{status}\n\n{suggestion}")
    except Exception as e:
        await update.message.reply_text("⚠️ Couldn't connect to the server. Try again later.")

# Handle photo uploads
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        photo_bytes = await file.download_as_bytearray()

        files = {'image': ('screenshot.jpg', BytesIO(photo_bytes), 'image/jpeg')}
        response = requests.post("http://127.0.0.1:5000/image-check", files=files, timeout=5)
        result = response.json()
        await update.message.reply_text(result.get("result", "No result returned."))
    except Exception as e:
        await update.message.reply_text("⚠️ Error analyzing image. Please try again later.")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app.run_polling()
