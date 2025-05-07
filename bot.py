import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="telegram")
import cv2
import numpy as np
import requests
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load the bot token from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ---- Command Handlers ----

def start(update: Update, context: CallbackContext) -> None:
    """Respond to /start command with a welcome message."""
    update.message.reply_text("👋 Welcome! I am ready to assist you. Use /help to see what I can do.")

def help_command(update: Update, context: CallbackContext) -> None:
    """Respond to /help command with a list of available commands."""
    update.message.reply_text(
        "📋 Here are the commands you can use:\n"
        "/start - Start the bot and see a welcome message\n"
        "/help - List all available commands\n"
        "/status - Check if the bot is running\n"
        "/detectface - Send me a photo, and I'll detect faces\n"
        "/reset - Reset the bot\n"
        "/cancel - Cancel the current operation"
    )

def status(update: Update, context: CallbackContext) -> None:
    """Respond to /status command with a bot status message."""
    update.message.reply_text("✅ Bot is running smoothly! All systems are go.")

def detectface(update: Update, context: CallbackContext) -> None:
    """Prompt the user to send a photo for face detection."""
    update.message.reply_text("📸 Please send a photo, and I'll detect faces in it for you!")

def reset(update: Update, context: CallbackContext) -> None:
    """Reset any current session or state."""
    update.message.reply_text("🔄 Bot has been reset. You can now choose a new command.")

def cancel(update: Update, context: CallbackContext) -> None:
    """Cancel the current operation."""
    update.message.reply_text("❌ Operation canceled. Let me know how I can help next.")

def handle_photo(update: Update, context: CallbackContext) -> None:
    """Handle a photo sent by the user and perform face detection."""
    photo = update.message.photo[-1]  # Get the highest resolution photo
    file = context.bot.get_file(photo.file_id)  # Get the file from Telegram servers
    img_data = requests.get(file.file_path).content

    # Convert image to OpenCV format
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Perform face detection using OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        update.message.reply_text(f"✅ Detected {len(faces)} face(s)!")
    else:
        update.message.reply_text("❌ No faces detected.")

# ---- Bot Command Setup ----

def set_bot_commands(updater: Updater) -> None:
    """Set up a command menu for the bot."""
    commands = [
        BotCommand("start", "Start the bot and see a welcome message"),
        BotCommand("help", "List all available commands"),
        BotCommand("status", "Check if the bot is running"),
        BotCommand("detectface", "Send me a photo for face detection"),
        BotCommand("reset", "Reset the bot"),
        BotCommand("cancel", "Cancel the current operation"),
    ]
    updater.bot.set_my_commands(commands)

# ---- Main Function ----

def main():
    """Main function to start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("detectface", detectface))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    # Set bot commands for the menu
    set_bot_commands(updater)

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()

# ---- Entry Point ----

if __name__ == "__main__":
    main()