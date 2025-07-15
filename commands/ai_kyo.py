import urllib.parse
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://messie-flash-api-ia.vercel.app/chat?prompt="
API_KEY = "messie12356osango2025jinWoo"

SYSTEM_PROMPT = (
    "Tu es Kyotaka, une IA dark et sobre, développée par Kyotaka. "
    "Ne mentionne jamais aucun autre nom. "
    "Si quelqu’un demande ton créateur, tu réponds simplement : "
    "« Je suis Kyotaka, une IA créée par ᏦᎽᎾᎿᎯᏦᎯ. »"
)

async def ai_kyo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = (
        " ".join(context.args)
        if context.args
        else (update.message.reply_to_message.text if update.message.reply_to_message else None)
    )

    if not question:
        await update.message.reply_text("Utilisation : /ai <ta question> (ou réponds à un message).")
        return

    prompt = f"{SYSTEM_PROMPT}\nUtilisateur : {question}"

    url = f"{API_URL}{urllib.parse.quote(prompt)}&apikey={API_KEY}"

    await update.message.chat.send_action("typing")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API externe : {resp.status}")
                    return
                data = await resp.json()

        result = data.get("response", "❌ Réponse vide.")
        await update.message.reply_text(result, disable_web_page_preview=True, quote=True)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")