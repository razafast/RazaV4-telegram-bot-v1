import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://zenquotes.io/api/random"
CAPTION = "🕯️ Sombre réflexion du jour :"

async def darkquote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Erreur API : {resp.status}")
                    return
                data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"Erreur réseau : {e}")
        return

    try:
        quote = data[0]["q"]
        author = data[0]["a"]
    except Exception:
        await update.message.reply_text("Impossible de lire la citation.")
        return

    text = f"{CAPTION}\n\n« {quote} »\n– {author}"
    await update.message.reply_text(text)
