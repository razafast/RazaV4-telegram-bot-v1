# commands/ass.py

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "wPFeQbmfRV-rpzlhttqX7nY7tDBMnN6-Tx72EqzIEQ"
API_URL = "https://api.night-api.com/images/nsfw/ass"
CAPTION = "🍑 Voilà des ass"

async def ass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {"authorization": API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as resp:
            if resp.status != 200:
                await update.message.reply_text(f"Erreur API : {resp.status}")
                return

            json = await resp.json()
            url = json.get("content", {}).get("url")

            if not url:
                await update.message.reply_text("Aucune image reçue 😕")
                return

            await update.message.reply_photo(photo=url, caption=CAPTION)
