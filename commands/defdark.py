from telegram import Update
from telegram.ext import ContextTypes

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🖤 *defdark* - Définitions dark en anglais uniquement.\n\n"
            "Utilisation : /defdark <mot>\n"
            "Exemple : /defdark shadow\n\n"
            "_Note : La définition est en anglais._",
            parse_mode="Markdown"
        )
        return

    word = context.args[0]
    await update.message.reply_text(f"Recherche de la définition sombre pour *{word}*...", parse_mode="Markdown")
    
    import aiohttp
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if resp.status != 200:
            await update.message.reply_text(f"❌ Mot introuvable ou erreur API ({resp.status})")
            return
        data = await resp.json()
        try:
            definition_en = data[0]["meanings"][0]["definitions"][0]["definition"]
        except (IndexError, KeyError):
            await update.message.reply_text("❌ Impossible de récupérer la définition.")
            return

    dark_msg = (
        f"⚫ *Définition dark de* `{word}` :\n\n"
        f"🖤 {definition_en}"
    )

    await update.message.reply_text(dark_msg, parse_mode="Markdown")
