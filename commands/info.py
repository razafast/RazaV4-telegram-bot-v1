from telegram import Update
from telegram.ext import ContextTypes

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Renvoie l’ID, le nom, le username et la photo de profil de l’utilisateur ciblé :
    • si tu réponds à son message ;
    • sinon si tu passes /info @username ou /info <id> ;
    • sinon c’est toi-même.
    """
    
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args:
        try:
            
            user = (await context.bot.get_chat_member(
                update.effective_chat.id,
                context.args[0]
            )).user
        except Exception:
            await update.message.reply_text("Utilisateur introuvable.")
            return
    else:
        user = update.effective_user

    
    text = (
        f"🆔 ID : <code>{user.id}</code>\n"
        f"👤 Nom : {user.full_name}\n"
        f"🔗 Username : @{user.username if user.username else '—'}"
    )

    
    photos = await context.bot.get_user_profile_photos(user.id, limit=1)
    if photos.total_count:
        
        file_id = photos.photos[0][-1].file_id
        await update.message.reply_photo(file_id, caption=text, parse_mode="HTML")
    else:
        await update.message.reply_html(text)
