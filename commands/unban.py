# commands/unban.py
from telegram import Update
from telegram.ext import ContextTypes

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /unban : débannit un membre du groupe.
    ▸ Méthode la plus simple : répondre à l’un de ses anciens messages.
    ▸ Sinon : /unban <id> ou /unban @username
    Le bot doit être admin et avoir le droit « Peut bannir ».
    """
    chat_id = update.effective_chat.id

    # ─── Trouver la cible ────────────────────────────────────────────────
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = context.args[0]
    else:
        await update.message.reply_text("Utilisation : /unban en réponse ou /unban <id|@user>")
        return

    # ─── Tentative de débannissement ────────────────────────────────────
    try:
        await context.bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
        await update.message.reply_text("✅ Utilisateur débanni avec succès.")
    except Exception as e:
        await update.message.reply_text(f"❌ Impossible de débannir : {e}")