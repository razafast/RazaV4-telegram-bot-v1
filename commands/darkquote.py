import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "wPFeQbmfRV-rpzlhttqX7nY7tDBMnN6-Tx72EqzIEQ"
API_URL = "https://api.night-api.com/generate/gemini"

PROMPT = (
    "Tu es une IA sombre. Génére une citation courte, profonde, mystérieuse ou mélancolique. "
    "Langue : français. Pas d'émoji, juste le texte brut."
)

async def darkquote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Invocation d'une citation obscure...")

    payload = {
        "prompt": PROMPT,
        "temperature": 0.8
    }
    headers = {"authorization": API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API : {resp.status}")
                    return
                data = await resp.json()
                quote = data.get("result", "…")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    await update.message.reply_text(f"💭 {quote}")
