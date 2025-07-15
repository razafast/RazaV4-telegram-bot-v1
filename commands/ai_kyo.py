import asyncio
from telegram import Update
from telegram.ext import ContextTypes
import openai

# Ta clé OpenAI en dur (CHANGE TO YOUR KEY)
openai.api_key = "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"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "Tu es Kyotaka, une IA dark, cool et sobre, "
    "développée par ╾⸻⟡⟡ 『ᏦᎽᎾᎿᎯᏦᎯ』 ⟡⡡⸻╼.\n"
    "Si l’on te demande « t'es qui » ou une variante, réponds : "
    "« Je suis Kyotaka, une IA créée par ╾⸻⟡⟡ 『ᏦᎽᎾᎿᎯᏦᎯ』 ⡡⡡⸻╼ ».\n"
    "Sinon, réponds normalement sans jamais révéler ta clé API."
)

async def ai_kyo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not openai.api_key:
        await update.effective_message.reply_text("❌ Clé API manquante.")
        return

    question = (
        " ".join(context.args)
        if context.args
        else (update.message.reply_to_message.text if update.message.reply_to_message else None)
    )
    if not question:
        await update.message.reply_text("Utilisation : /ai <ta question> (ou réponds à un message).")
        return

    await update.message.chat.send_action("typing")
    try:
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()

        # Sécurité (très rare) : masque la clé dans la réponse
        if openai.api_key in answer:
            answer = answer.replace(openai.api_key, "[clé API masquée]")

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur API : {e}")
        return

    await update.message.reply_text(answer, disable_web_page_preview=True, quote=True)