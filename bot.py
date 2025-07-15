import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
)

from commands.kick import kick
from commands.help_cmd import help_command
from commands.info import info
from commands.ttp import ttp
from commands.lirik import lirik
from commands.ytmp4 import ytmp4
from commands.ipinfo import ipinfo

TOKEN = "8146852566:AAHf8Jkrd124pWD1N6G9AeOKxtGIi3gvouA"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes."
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # commandes de base
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # admin
    app.add_handler(CommandHandler("kick", kick))

    # utilitaires
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("ipinfo", ipinfo))

    # fun / media
    app.add_handler(CommandHandler("ttp", ttp))
    app.add_handler(CommandHandler("lirik", lirik))
    app.add_handler(CommandHandler("ytmp4", ytmp4))

    print("✅ Bot lancé.")
    app.run_polling()