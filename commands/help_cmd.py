from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    text = """
🧠 *Commandes disponibles :*

/start - Démarrer le bot
/help - Voir les commandes
/kick - Expulser un utilisateur (admin uniquement)
/rps - Jeu pierre feuille ciseaux
"""
    await update.message.reply_text(text, parse_mode="Markdown")
