from telegram import Update, ChatMemberAdministrator, ChatMemberOwner
from telegram.ext import CallbackContext

async def kick(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    msg = update.effective_message

    if not msg.reply_to_message:
        await msg.reply_text("❌ Réponds au message de la personne à expulser.")
        return

    user_to_kick = msg.reply_to_message.from_user
    chat_id = chat.id

    # Vérifie si le bot est admin
    bot_member = await bot.get_chat_member(chat_id, bot.id)
    if not (bot_member.can_restrict_members if hasattr(bot_member, 'can_restrict_members') else False):
        await msg.reply_text("❌ Je dois être admin avec le droit d'expulser les membres.")
        return

    # Optionnel : vérifier si l'auteur est aussi admin
    sender = await bot.get_chat_member(chat_id, msg.from_user.id)
    if isinstance(sender, ChatMemberAdministrator) or isinstance(sender, ChatMemberOwner):
        try:
            await bot.ban_chat_member(chat_id, user_to_kick.id)
            await msg.reply_text(f"✅ {user_to_kick.mention_html()} a été expulsé du groupe.", parse_mode="HTML")
        except Exception as e:
            await msg.reply_text(f"❌ Erreur lors de l'expulsion : {e}")
    else:
        await msg.reply_text("❌ Seuls les admins peuvent utiliser cette commande.")