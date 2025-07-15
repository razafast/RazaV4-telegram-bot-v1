# commands/lirik.py
import urllib.parse
from telegram import Update
from telegram.ext import ContextTypes
import aiohttp

API_KEY = "d90a9e986e18778b"

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cherche les paroles d’une chanson avec /lirik <titre>"""

    if not context.args:
        await update.message.reply_text("Utilisation : /lirik <titre de la chanson>")
        return

    query = " ".join(context.args)
    url = f"https://api.xteam.xyz/lirik?lagu={urllib.parse.quote(query)}&apikey={API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await update.message.reply_text("❌ Aucune parole trouvée.")
                return
            data = await resp.json()

    title = data.get("title", "Titre inconnu")
    lyrics = data.get("lirik", "Paroles introuvables")

    # Découpe si trop long
    if len(lyrics) > 4000:
        lyrics = lyrics[:4000] + "\n...\n(Paroles coupées)"

    await update.message.reply_text(
        f"🎶 <b>{title}</b>\n\n<pre>{lyrics}</pre>",
        parse_mode="HTML"
    )