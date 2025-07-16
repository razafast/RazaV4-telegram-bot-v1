from telegram import Update, ChatMember
from telegram.ext import ContextTypes

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        user_name = member.full_name
        group_name = update.effective_chat.title

        message = (
            f"🕶️ Bienvenue à toi, {user_name}.\n"
            f"Tu viens d’entrer dans {group_name}...\n"
            f"Ici, chaque silence a un sens.\n"
            f"Marche sans bruit, observe sans parler.\n"
            f"Seuls les esprits éveillés comprennent ce lieu."
        )

        await update.message.reply_text(message)