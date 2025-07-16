# commands/ban.py

from telegram import Update, ChatMember
from telegram.ext import ContextTypes

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Réponds au message de l'utilisateur à bannir.")
        return

    user_to_ban = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_to_ban.id
        )
        await update.message.reply_text(
            f"🔨 {user_to_ban.first_name} a été banni de ce groupe."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Impossible de bannir : {e}")