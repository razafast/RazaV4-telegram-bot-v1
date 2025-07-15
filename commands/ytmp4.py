# commands/ytmp4.py
import urllib.parse
from telegram import Update
from telegram.ext import ContextTypes
import aiohttp

API_KEY = "d90a9e986e18778b"

async def ytmp4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Télécharge une vidéo YouTube avec /ytmp4 <lien>"""

    if not context.args:
        await update.message.reply_text("Utilisation : /ytmp4 <lien YouTube>")
        return

    link = context.args[0]
    url = f"https://api.xteam.xyz/dl/ytmp4?url={urllib.parse.quote(link)}&apikey={API_KEY}"

    await update.message.reply_text("⏳ Téléchargement en cours...")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await update.message.reply_text("❌ Impossible de télécharger la vidéo.")
                return
            data = await resp.json()

    result = data.get("result", {})
    title = result.get("title", "Vidéo")
    video_url = result.get("url")

    if not video_url:
        await update.message.reply_text("❌ Aucun lien vidéo trouvé.")
        return

    try:
        await update.message.reply_video(
            video=video_url,
            caption=f"🎬 {title}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l'envoi de la vidéo : {e}")