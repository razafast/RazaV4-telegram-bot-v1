import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

from commands.kick import kick
from commands.rps import rps
from commands.help_cmd import help_command
from commands.info import info               # ← NEW

# Remplace par ton vrai token ici
TOKEN = "8146852566:AAHf8Jkrd124pWD1N6G9AeOKxtGIi3gvouA"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes."
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("rps", rps))
    app.add_handler(CommandHandler("info", info))    # ← NEW

    print("✅ Bot lancé.")
    app.run_polling()