import urllib.parse
from io import BytesIO
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "d90a9e986e18778b"

async def ttp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        text = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        text = update.message.reply_to_message.text
    else:
        await update.message.reply_text("Utilisation : /ttp <texte> (ou réponds à un message).")
        return

    base_url = "https://api.xteam.xyz/ttp"
    params = {
        "file": "true",
        "text": text,
        "apikey": API_KEY,
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await update.message.reply_text("🚫 L’API XTeam a renvoyé une erreur.")
                    return
                data = await resp.read()
    except aiohttp.ClientError:
        await update.message.reply_text("🚫 Erreur réseau lors de la requête à l’API XTeam.")
        return

    await update.message.reply_photo(
        photo=BytesIO(data),
        filename="ttp.png",
        caption="🖼️ Sticker généré par XTeam"
    )