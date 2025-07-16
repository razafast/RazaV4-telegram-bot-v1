import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Utilisation : /defdark <mot>")
        return

    word = context.args[0]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(word)) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Mot introuvable ou erreur API ({resp.status})")
                    return
                data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    try:
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        example = data[0]["meanings"][0]["definitions"][0].get("example", "Aucun exemple.")
    except Exception:
        await update.message.reply_text("❌ Erreur lors de l’analyse de la réponse.")
        return

    text = f"📚 Définition dark de : *{word}*\n\n🖤 {meaning}\n\n💬 _{example}_"
    await update.message.reply_text(text, parse_mode="Markdown")
