import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "14960d2b4c71e3b190761233"
API_URL = "https://api.lolhuman.xyz/api/random/nsfw/boobs"  # <- corrigé

async def boobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {"apikey": API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Erreur API: {resp.status}")
                    return

                data = await resp.json()
                image_url = data.get("result")

                if not image_url:
                    await update.message.reply_text("Aucune image reçue 😕")
                    return

                await update.message.reply_photo(photo=image_url, caption="Voici tes boobs 😏")

    except Exception as e:
        await update.message.reply_text(f"Erreur réseau : {e}")