import aiohttp
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "d90a9e986e18778b"   # ta clé XTeam

async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie une image NSFW aléatoire dans n’importe quel chat (PV, groupe, canal)."""

    msg = update.effective_message      # fonctionne pour message ou channel_post
    chat_id = update.effective_chat.id

    await msg.reply_text("🔞 Recherche d’une image NSFW…")

    url = f"https://api.xteam.xyz/hentai?file=true&apikey={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await msg.reply_text("❌ Impossible de récupérer l’image.")
                return
            data = await resp.read()

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=BytesIO(data),
        caption="🔞 Contenu NSFW fourni par XTeam"
    )