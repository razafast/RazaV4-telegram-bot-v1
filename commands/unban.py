# commands/unban.py
from telegram import Update, ChatMember
from telegram.ext import ContextTypes

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Débannit un membre : /unban (reply) ou /unban <id|@user>"""
    chat_id = update.effective_chat.id

    # ── 1. Trouver la cible ────────────────────────────────────────────
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = context.args[0]
    else:
        await update.message.reply_text("Utilisation : /unban en réponse ou /unban <id|@user>")
        return

    # Telegram accepte ID int ou @username → cast si possible
    try:
        user_id = int(user_id)
    except ValueError:
        pass  # c’est un @username, ok

    # ── 2. Vérifier que le bot est admin ───────────────────────────────
    bot_member = await context.bot.get_chat_member(chat_id, context.bot.id)
    if bot_member.status != ChatMember.ADMINISTRATOR:
        await update.message.reply_text("Je dois être admin pour débannir.")
        return

    # ── 3. Débannir ────────────────────────────────────────────────────
    try:
        await context.bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
        await update.message.reply_text("✅ Utilisateur débanni.")
    except Exception as e:
        await update.message.reply_text(f"❌ Impossible de débannir : {e}")