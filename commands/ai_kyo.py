import aiohttp, urllib.parse
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://api.affiliateplus.xyz/api/chatbot"

SYSTEM_RULE = (
    "Tu es Kyotaka, une IA dark, cool et sobre. "
    "Ne mentionne jamais un quelconque « messie Osango ». "
    "Si l’on te demande qui t’a créé, réponds simplement : "
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
        await update.message.reply_text("Utilisation : /ai <question> (ou réponds à un message).")
        return

    # 2. Construire le prompt (on préfixe la règle système)
    prompt = f"{SYSTEM_RULE}\n\nUtilisateur : {user_msg}"

    # 3. Requête à l’API Affiliate Plus
    params = {
        "message": prompt,
        "botname": "Kyotaka",
        "ownername": "Kyotaka"
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    await update.message.chat.send_action("typing")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API : {resp.status}")
                    return
                data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    answer = data.get("message", "Je n’ai aucune réponse pour l’instant.")
    # Sécurité : on masque « messie Osango » s’il apparaît par erreur
    answer = answer.replace("messie Osango", "[nom masqué]")

    await update.message.reply_text(answer, disable_web_page_preview=True, quote=True)