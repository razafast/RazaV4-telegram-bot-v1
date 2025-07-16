import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Utilisation : /defdark <mot>")

    word = context.args[0]
    await update.message.reply_text(f"🕯️ Recherche de la définition sombre pour *{word}*...", parse_mode="Markdown")

    async with aiohttp.ClientSession() as session:
        # Récupérer la définition en anglais
        resp = await session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if resp.status != 200:
            return await update.message.reply_text(f"❌ Mot introuvable ou erreur API ({resp.status})")
        data = await resp.json()
        definition_en = data[0]["meanings"][0]["definitions"][0]["definition"]

        # Traduction via LibreTranslate stable
        translate_url = "https://libretranslate.de/translate"
        payload = {
            "q": definition_en,
            "source": "en",
            "target": "fr",
            "format": "text"
        }

        try:
            async with session.post(translate_url, json=payload, timeout=10) as trans:
                if trans.status != 200:
                    return await update.message.reply_text("❌ Erreur lors de la traduction.")
                result = await trans.json()
                definition_fr = result.get("translatedText")
        except Exception:
            return await update.message.reply_text("❌ Erreur lors de la traduction.")

    await update.message.reply_text(
        f"📚 Définition dark de *{word}* :\n\n🖤 {definition_fr}",
        parse_mode="Markdown"
    )
