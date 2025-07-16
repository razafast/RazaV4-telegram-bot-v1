import os, aiohttp, urllib.parse
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = os.getenv("AIzaSyDbLr0gx5ldIDqxXt9D0iUl77fGUI-QDEM")          # ← mets ta clé ici, ou en env
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-pro:generateContent?key="
    + urllib.parse.quote(API_KEY)              # clé dans l’URL (format Google)
)

SYSTEM_RULE = (
    "Tu es Kyotaka, une IA dark, cool et sobre. "
    "Ne mentionne jamais un quelconque « messie Osango ». "
    "Si l’on te demande qui t’a créé, réponds : "
    "« Je suis Kyotaka, IA développée par ᏦᎽᎾᎿᎯᏦᎯ. » "
    "Réponds normalement à tout le reste."
)

async def ai_kyo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. Récupérer la question
    if context.args:
        user_msg = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        user_msg = update.message.reply_to_message.text
    else:
        await update.message.reply_text(
            "Utilisation : /ai <question> (ou réponds à un message)."
        )
        return

    prompt = f"{SYSTEM_RULE}\n\nUtilisateur : {user_msg}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": { "temperature": 0.7 }
    }

    await update.message.chat.send_action("typing")

    if not API_KEY:
        await update.message.reply_text("❌ Clé GEMINI_API_KEY manquante.")
        return

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            async with s.post(API_URL, json=payload) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur Gemini : {resp.status}")
                    return
                data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    # Gemini renvoie la réponse dans choices[0].content.parts[0].text
    try:
        answer = (
            data["candidates"][0]["content"]["parts"][0]["text"]
        )
    except (KeyError, IndexError):
        answer = "Je n’ai aucune réponse pour l’instant."

    answer = answer.replace("messie Osango", "[nom masqué]")

    await update.message.reply_text(
        answer, disable_web_page_preview=True, quote=True
    )