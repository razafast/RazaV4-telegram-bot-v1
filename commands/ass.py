import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://api.waifu.pics/nsfw/ass"
CAPTION = "Voici un 🍑 bien juteux 😏"

async def ass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Erreur API : {resp.status}")
                    return

                data = await resp.json()
                image_url = data.get("url")  # ✅ waifu.pics utilise "url"

                if not image_url:
                    await update.message.reply_text("Pas d'image reçue 😕")
                    return

                await update.message.reply_photo(photo=image_url, caption=CAPTION)

    except Exception as e:
        await update.message.reply_text(f"Erreur réseau : {e}")