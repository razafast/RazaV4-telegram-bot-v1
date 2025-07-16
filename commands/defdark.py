import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Utilisation : /defdark <mot>")
        return

    word = context.args[0]

    try:
        async with aiohttp.ClientSession() as session:
            # 1. Récupère la définition (en anglais)
            async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Mot introuvable ou erreur API ({resp.status})")
                    return
                data = await resp.json()
            definition_en = data[0]["meanings"][0]["definitions"][0]["definition"]

            # 2. Traduire la définition en français via LibreTranslate (open-source)
            translate_payload = {
                "q": definition_en,
                "source": "en",
                "target": "fr",
                "format": "text"
            }
            async with session.post("https://libretranslate.com/translate", json=translate_payload) as trans_resp:
                if trans_resp.status != 200:
                    await update.message.reply_text("❌ Erreur lors de la traduction.")
                    return
                trans_data = await trans_resp.json()
                definition_fr = trans_data["translatedText"]

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    await update.message.reply_text(f"📚 Définition dark de *{word}* :\n\n🖤 {definition_fr}", parse_mode="Markdown")
