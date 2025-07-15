from telegram import Update, ChatMemberAdministrator, ChatMemberOwner
from telegram.ext import CallbackContext

async def kick(update: Update, context: CallbackContext):
    # Vérifie si on a bien répondu à un message
    if not update.message.reply_to_message:
        await update.message.reply_text("Réponds au message de la personne à expulser.")
        return

    chat = update.effective_chat
    bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
    target_user = update.message.reply_to_message.from_user
    target_member = await context.bot.get_chat_member(chat.id, target_user.id)

    # Vérifie si le bot est admin
    if not (bot_member.status == "administrator" and bot_member.can_restrict_members):
        await update.message.reply_text("Je dois être administrateur avec les droits d’expulsion.")
        return

    # Empêche d’expulser un admin ou le propriétaire
    if target_member.status in [ChatMemberAdministrator.STATUS, ChatMemberOwner.STATUS]:
        await update.message.reply_text("Je ne peux pas expulser un administrateur.")
        return

    try:
        await context.bot.ban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(f"{target_user.mention_html()} a été expulsé du groupe. 🦾", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"Erreur : impossible d’expulser cet utilisateur.\n{e}")