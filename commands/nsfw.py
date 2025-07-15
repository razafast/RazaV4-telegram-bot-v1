import aiohttp
from telegram import Update
from telegram.ext import ContextTypes
from io import BytesIO

API_URL = "https://delirius-apiofc.vercel.app/nsfw/girls"

async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie une image NSFW aléatoire depuis Delirius API (PV, groupe, canal)."""

    msg = update.effective_message
    chat_id = update.effective_chat.id

    await msg.reply_text("🔞 Recherche d’une image NSFW…")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                if resp.status != 200:
                    await msg.reply_text("❌ Impossible de récupérer l’image.")
                    return
                image_data = await resp.read()
    except Exception as e:
        await msg.reply_text(f"❌ Erreur réseau : {e}")
        return

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=BytesIO(image_data),
        caption="🔞 Contenu NSFW fourni par Delirius API"
    )