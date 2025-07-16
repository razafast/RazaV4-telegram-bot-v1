# cmds/kick.py  
from telegram import Update, ChatMember
from telegram.ext import ContextTypes

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bannit un utilisateur (réponse ou argument). Fonctionne en groupe normal ou supergroupe."""

    
    target_user = None
    if update.message.reply_to_message:                        
        target_user = update.message.reply_to_message.from_user
    elif context.args:                                         
        try:
            
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

    
    bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
    target_member = await context.bot.get_chat_member(update.effective_chat.id, target_user.id)

    
    if not (bot_member.status == ChatMember.ADMINISTRATOR and bot_member.can_restrict_members):
        await update.message.reply_text("Je dois être admin avec le droit d'expulser.")
        return

    
    if target_member.status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER):
        await update.message.reply_text("Je ne peux pas expulser un administrateur du groupe.")
        return

    
    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target_user.id,
            revoke_messages=True      
        )
        await update.message.reply_html(f"🚫 <b>{target_user.mention_html()}</b> a été banni.")
    except Exception as e:
        
        await update.message.reply_text(f"❌ Impossible de bannir : {e}")
