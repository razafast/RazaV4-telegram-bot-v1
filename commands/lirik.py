"""Commande /lirik — Récupère les paroles d'une chanson via lyrics.ovh (API sans clé).

Utilisation : /lirik <artiste> - <titre>
Exemples :
    /lirik eminem - lose yourself
    /lirik eminem lose yourself

Si aucun tiret n'est fourni, le premier mot est pris comme artiste
et le reste comme titre.
"""

import urllib.parse
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

MAX_TELEGRAM_CHARS = 4000  # limite de caractères pour Telegram

API_BASE = "https://api.lyrics.ovh/v1/{artist}/{title}"

def _parse_query(query: str) -> tuple[str, str] | None:
    """Détermine (artist, title) à partir d'une chaîne entrée par l'utilisateur."""
    if "-" in query:
        artist, title = map(str.strip, query.split("-", 1))
        if artist and title:
            return artist, title
    else:
        parts = query.split()
        if len(parts) >= 2:
            artist = parts[0]
            title = " ".join(parts[1:])
            return artist, title
    return None


async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1️⃣ Récupère la requête utilisateur
    if context.args:
        query = " ".join(context.args)
    else:
        await update.effective_message.reply_text(
            "Utilisation : /lirik <artiste> - <titre>"
        )
        return

    parsed = _parse_query(query)
    if not parsed:
        await update.effective_message.reply_text(
            "Format invalide. Exemple : /lirik eminem - lose yourself"
        )
        return

    artist, title = parsed
    await update.effective_message.reply_text("🔍 Recherche des paroles…")

    # 2️⃣ Appel API
    url = API_BASE.format(
        artist=urllib.parse.quote(artist, safe=""),
        title=urllib.parse.quote(title, safe=""),
    )

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                elif resp.status == 404:
                    await update.effective_message.reply_text("❌ Paroles introuvables.")
                    return
                else:
                    await update.effective_message.reply_text(
                        f"❌ Erreur API ({resp.status})."
                    )
                    return
    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erreur réseau : {e}")
        return

    lyrics = data.get("lyrics", "Paroles introuvables")

    if len(lyrics) > MAX_TELEGRAM_CHARS:
        lyrics = lyrics[:MAX_TELEGRAM_CHARS] + "\n...\n(Paroles coupées)"

    await update.effective_message.reply_text(
        f"🎶 <b>{artist.title()} – {title.title()}</b>\n\n<pre>{lyrics}</pre>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )