import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://pollinations.ai/p/"

async def darkgen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Utilisation : /darkgen <description>")

    prompt = " ".join(context.args)
    url = API_URL + aiohttp.helpers.quote(prompt)

    await update.message.reply_text("🕯️ Génération en cours...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await update.message.reply_text(f"❌ Erreur API : {resp.status}")

                img_data = await resp.read()
                return await update.message.reply_photo(photo=img_data, caption="🌒 Image générée")
    except Exception as e:
        return await update.message.reply_text(f"❌ Erreur réseau : {e}")
