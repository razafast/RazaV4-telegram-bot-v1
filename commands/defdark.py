import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "wPFeQbmfRV-rpzlhttqX7nY7tDBMnN6-Tx72EqzIEQ"  
API_URL = "https://api.night-api.com/generate/gemini"

SYSTEM_PROMPT = (
    "Tu es une entité sombre. Quand on te donne un mot, tu inventes une définition "
    "obscure, profonde, parfois métaphorique. Réponds uniquement en français."
)

async def defdark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Utilisation : /defdark <mot>")
        return

    word = " ".join(context.args)
    prompt = f"{SYSTEM_PROMPT}\n\nMot : {word}\nDéfinition :"

    await update.message.reply_text("🕯️ Définition occulte en cours...")

    payload = {"prompt": prompt, "temperature": 0.8}
    headers = {"authorization": API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API : {resp.status}")
                    return
                data = await resp.json()
                text = data.get("result", "Aucune réponse.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    await update.message.reply_text(
        f"📚 *Définition obscure de* `{word}` :\n\n{text}",
        parse_mode="Markdown"
    )
