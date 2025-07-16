"""Commande /hboobs — images hentai boobs."""

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "wPFeQbmfRV-rpzlhttqX7nY7tDBMnN6-Tx72EqzIEQ"
API_URL = "https://api.night-api.com/images/nsfw/hboobs"
CAPTION = "🍈 Hentai dark boobs invoqués..."

async def hboobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {"authorization": API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, headers=headers) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Erreur API : {resp.status}")
                    return

                data = await resp.json()
                image_url = data.get("content", {}).get("url")

                if not image_url:
                    await update.message.reply_text("Aucune image reçue 😕")
                    return

                await update.message.reply_photo(photo=image_url, caption=CAPTION)
    except Exception as e:
        await update.message.reply_text(f"Erreur réseau : {e}")