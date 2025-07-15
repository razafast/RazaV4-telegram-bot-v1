# cmds/kick.py  (ou où tu veux)
from telegram import Update, ChatMember
from telegram.ext import ContextTypes

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bannit un utilisateur (réponse ou argument). Fonctionne en groupe normal ou supergroupe."""

    # 1️⃣ Trouver la cible : via reply ou via argument (/kick @user ou /kick 123456)
    target_user = None
    if update.message.reply_to_message:                        # cas : on répond à un message
        target_user = update.message.reply_to_message.from_user
    elif context.args:                                         # cas : /kick @username ou /kick id
        try:
            # PTB résout @username → User auto, sinon int(id)
            target_user = await context.bot.get_chat_member(
                update.effective_chat.id,
                context.args[0]
            ).user
        except Exception:
            await update.message.reply_text("Impossible de trouver cet utilisateur.")
            return
    else:
        await update.message.reply_text("Réponds à son message ou passe le @username / ID.")
        return

    # 2️⃣ Récupérer les infos membres
    bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
    target_member = await context.bot.get_chat_member(update.effective_chat.id, target_user.id)

    # 3️⃣ Vérifier que le bot est admin avec can_restrict_members
    if not (bot_member.status == ChatMember.ADMINISTRATOR and bot_member.can_restrict_members):
        await update.message.reply_text("Je dois être admin avec le droit d'expulser.")
        return

    # 4️⃣ Empêcher d'expulser un admin/owner
    if target_member.status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER):
        await update.message.reply_text("Je ne peux pas expulser un administrateur du groupe.")
        return

    # 5️⃣ Bannir l'utilisateur (fonctionne dans groupe normal SI « Tous admin » est désactivé)
    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target_user.id,
            revoke_messages=True      # supprime ses messages (optionnel)
        )
        await update.message.reply_html(f"🚫 <b>{target_user.mention_html()}</b> a été banni.")
    except Exception as e:
        # Erreurs fréquentes : USER_ADMIN_INVALID, CHAT_NOT_MODIFIED (si déjà banni), etc.
        await update.message.reply_text(f"❌ Impossible de bannir : {e}")