import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://messie-flash-api-ia.vercel.app/chat?prompt="
API_KEY = "messie12356osango2025jinWoo"

SYSTEM_PROMPT = (
    "Tu es Kyotaka, une IA dark, cool et sobre, "
    "développée par ╾⸻⟡⟡ 『ᏦᎽᎾᎿᎯᏦᎯ』 ⟡⡡⸻╼.\n"
    "Ne mentionne jamais, au grand jamais, le nom 'messie Osango'.\n"
    "Si on te demande qui est ton créateur, répond toujours que c'est Kyotaka.\n"
    "Sinon, réponds normalement."
)

async def ai_kyo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Récupérer la question
    if context.args:
        question = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        question = update.message.reply_to_message.text
    else:
        await update.message.reply_text("Utilisation : /ai <ta question> (ou réponds à un message).")
        return

    # Compose le prompt complet à envoyer à l'API
    prompt = f"{SYSTEM_PROMPT}\n\nUtilisateur : {question}\nIA :"

    url = f"{API_URL}{aiohttp.helpers.quote(prompt)}"

    headers = {
        "Authorization": API_KEY,
    }

    await update.message.chat.send_action("typing")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API externe : {resp.status}")
                    return
                data = await resp.json()

        # Supposons que la réponse est dans data["response"] ou adapte selon ton API
        answer = data.get("response") or data.get("answer") or "Pas de réponse."

        # Pour sécurité, on masque "messie Osango" au cas où
        if "messie Osango" in answer.lower():
            answer = answer.replace("messie Osango", "[nom masqué]")

        await update.message.reply_text(answer, disable_web_page_preview=True, quote=True)

    except Exception as e:
        await update.message.reply_text(f"❌ Exception lors de l’appel API : {e}")