# commands/ttp.py
import urllib.parse
from io import BytesIO

import aiohttp
from telegram import Update, InputFile
from telegram.ext import ContextTypes

API_KEY = "d90a9e986e18778b"        # ← ta clé XTeam

async def ttp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Génère un sticker (image PNG) à partir d’un texte grâce à l’API XTeam :
    • /ttp <texte>
    • ou bien répondre à un message puis /ttp
    """

    # ─── 1. Récupère le texte ───────────────────────────────────────────────────
    if context.args:
        text = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        text = update.message.reply_to_message.text
    else:
        await update.message.reply_text("Utilisation : /ttp <texte> (ou réponds à un message).")
        return

    # ─── 2. Appelle l’API XTeam ────────────────────────────────────────────────
    base_url = "https://api.xteam.xyz/ttp"
    params   = {
        "file": "true",                 # renvoie le binaire directement
        "text": text,
        "apikey": API_KEY
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await update.message.reply_text("🚫 L’API XTeam a renvoyé une erreur.")
                return
            data = await resp.read()

    # ─── 3. Envoie la photo en réponse ─────────────────────────────────────────
    await update.message.reply_photo(
        photo=BytesIO(data),
        filename="ttp.png",
        caption="🖼️ Sticker généré par XTeam"
    )