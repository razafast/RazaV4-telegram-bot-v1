# commands/defdark.py

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Utilisation : /defdark <mot>")

    word = context.args[0]
    await update.message.reply_text(f"🕯️ Recherche de la définition sombre pour *{word}*...", parse_mode="Markdown")

    async with aiohttp.ClientSession() as session:
        # 1. Récupérer la définition en anglais
        resp = await session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if resp.status != 200:
            return await update.message.reply_text(f"❌ Mot introuvable ou erreur API ({resp.status})")
        data = await resp.json()
        definition_en = data[0]["meanings"][0]["definitions"][0]["definition"]

        # 2. Traduire en français
        payload = {"q": definition_en, "source": "en", "target": "fr", "format": "text"}
        trans = await session.post("https://libretranslate.com/translate", json=payload)
        if trans.status != 200:
            return await update.message.reply_text("❌ Erreur lors de la traduction.")
        definition_fr = (await trans.json()).get("translatedText")

    await update.message.reply_text(f"📚 Définition dark de *{word}* :\n\n🖤 {definition_fr}", parse_mode="Markdown")
