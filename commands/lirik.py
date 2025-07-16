import urllib.parse, aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "14960d2b4c71e3b190761233"          # ← ta clé lolhuman
API_URL = "https://api.lolhuman.xyz/api/lirik"  # endpoint paroles

MAX_TELEGRAM_CHARS = 4000                      # limite message

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /lirik <titre ou artiste>   → Renvoie les paroles d’une chanson
    Peut être utilisé en privé, groupe, supergroupe ou canal.
    """

    # 1️⃣ récupérer la requête
    if context.args:
        query = " ".join(context.args)
    else:
        await update.effective_message.reply_text(
            "Utilisation : /lirik <titre ou artiste>"
        )
        return

    await update.effective_message.reply_text("🔍 Recherche des paroles…")

    # 2️⃣ appeler l’API lolhuman
    params = {"apikey": API_KEY, "query": query}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text(
                        f"❌ Erreur API ({resp.status})."
                    )
                    return
                data = await resp.json()
    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erreur réseau : {e}")
        return

    result = data.get("result", {})
    title  = result.get("title",  "Titre inconnu")
    lyrics = result.get("lirik",  "Paroles introuvables")

    # 3️⃣ couper si trop long (Telegram max 4096)
    if len(lyrics) > MAX_TELEGRAM_CHARS:
        lyrics = lyrics[:MAX_TELEGRAM_CHARS] + "\n...\n(Paroles coupées)"

    await update.effective_message.reply_text(
        f"🎶 <b>{title}</b>\n\n<pre>{lyrics}</pre>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )