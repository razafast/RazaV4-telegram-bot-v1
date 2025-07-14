from telegram import Update
from telegram.ext import CallbackContext

async def kick(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
        await update.message.reply_text("Réponds au message de la personne à expulser.")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Utilisateur expulsé. 🦾")
    except Exception as e:
        await update.message.reply_text("Erreur : je n’ai pas les droits nécessaires.")

