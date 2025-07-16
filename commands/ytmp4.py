import urllib.parse, aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "14960d2b4c71e3b190761233"          # ← ta clé lolhuman
API_URL = "https://api.lolhuman.xyz/api/ytvideo"

# Qualités préférées dans l’ordre (haute → basse)
PREFERRED_QUALITIES = ["720p", "480p", "360p", "240p"]

async def ytmp4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Télécharge une vidéo YouTube avec /ytmp4 <lien> (PV, groupe, canal)."""

    if not context.args:
        await update.message.reply_text("Utilisation : /ytmp4 <lien YouTube>")
        return

    yt_link = context.args[0]
    await update.effective_message.reply_text("⏳ Récupération des liens…")

    params = {"apikey": API_KEY, "url": yt_link}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"❌ Erreur API : {resp.status}")
                    return
                data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    result = data.get("result", {})
    title = result.get("title", "Vidéo")
    links = result.get("link", {})             # dict des qualités dispo

    # Choisir la meilleure qualité disponible
    video_url = None
    for q in PREFERRED_QUALITIES:
        if q in links:
            video_url = links[q]
            break
    # Fallback : premier lien mp4 trouvé
    if not video_url and isinstance(links, dict):
        video_url = next(iter(links.values()), None)

    if not video_url:
        await update.message.reply_text("❌ Aucun lien MP4 trouvé.")
        return

    await update.effective_message.reply_text("📤 Envoi de la vidéo…")

    try:
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=video_url,
            caption=f"🎬 {title}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l’envoi : {e}")