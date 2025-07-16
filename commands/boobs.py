import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "14960d2b4c71e3b190761233"
API_URL = "https://api.lolhuman.xyz/api/nsfw/boobs"

async def boobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {"apikey": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                image_url = data.get("result")
                if image_url:
                    await update.message.reply_photo(photo=image_url, caption="Voici tes boobs 😏")
                else:
                    await update.message.reply_text("Pas d'image retournée par l'API 😕")
            else:
                await update.message.reply_text("Erreur lors de la requête à l'API.")