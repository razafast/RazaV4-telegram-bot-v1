import aiohttp, urllib.parse, math
from telegram import Update
from telegram.ext import ContextTypes

LOL_API_KEY = "14960d2b4c71e3b190761233"
LOL_URL     = "https://api.lolhuman.xyz/api/ytvideo2"     # nouvel endpoint
AKU_URL     = "https://api.akuari.my.id/downloader/youtube?link={}"

PREFERRED_QUALITIES = ["720p", "480p", "360p", "240p"]
MAX_TELEGRAM_MB = 50                                      # limite d’envoi bot

async def _bytes_to_mb(size_str: str | int) -> float:
    """
    Convertit '12.3 MB' ou '12345' en méga-octets (float).
    """
    if isinstance(size_str, int):
        return size_str / 1_048_576
    num, unit = size_str.split()
    mul = {"KB": 1/1024, "MB": 1, "GB": 1024}.get(unit.upper(), 0)
    return float(num) * mul

async def ytmp4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /ytmp4 <lien YouTube>")
        return

    yt_link = context.args[0]
    await update.message.reply_text("⏳ Recherche des liens vidéo…")

    # ----- 1) essai LoL Human -------------------------------------------------
    try:
        params = {"apikey": LOL_API_KEY, "url": yt_link}
        lol_url = f"{LOL_URL}?{urllib.parse.urlencode(params)}"

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20)
        ) as session, session.get(lol_url) as resp:
            if resp.status == 200:
                data = await resp.json()
                result = data.get("result", {})
                title  = result.get("title", "Vidéo")
                links  = result.get("link", {})     # qualité → url
                sizes  = result.get("size", {})     # qualité → '12.3 MB'

                # choix de la meilleure qualité
                for q in PREFERRED_QUALITIES:
                    if q in links:
                        video_url = links[q]
                        size_mb = await _bytes_to_mb(sizes.get(q, "0 MB"))
                        break
                else:
                    video_url = next(iter(links.values()), None)
                    size_mb = 0

                if video_url:
                    if size_mb and size_mb <= MAX_TELEGRAM_MB:
                        await context.bot.send_video(
                            chat_id=update.effective_chat.id,
                            video=video_url,
                            caption=f"🎬 {title} ({q}, {size_mb:.1f} MB)"
                        )
                    else:
                        await update.message.reply_text(
                            f"🎬 {title}\nFichier ≈ {size_mb:.1f} MB – "
                            "voici le lien direct :\n" + video_url
                        )
                    return            # succès → on s’arrête ici
            else:
                # on continue vers la 2ᵉ API
                pass
    except Exception:
        # ignore pour passer au fallback
        pass

    # ----- 2) API de secours AkuAri ------------------------------------------
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20)
        ) as session, session.get(AKU_URL.format(urllib.parse.quote(yt_link))) as resp:
            if resp.status != 200:
                await update.message.reply_text(
                    f"❌ Échec (code {resp.status}) sur les deux APIs."
                )
                return
            data = await resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur réseau : {e}")
        return

    title = data.get("title", "Vidéo")
    # l’API retourne plusieurs itags ; on prend mp4 le plus léger
    videos = [v for v in data.get("mp4", []) if v.get("quality")]
    videos.sort(key=lambda v: PREFERRED_QUALITIES.index(v["quality"])
                               if v["quality"] in PREFERRED_QUALITIES else 99)
    if not videos:
        await update.message.reply_text("❌ Aucun lien MP4 trouvé.")
        return

    best = videos[0]
    video_url = best["url"]
    size_mb = await _bytes_to_mb(best.get("size", "0 MB"))

    if size_mb <= MAX_TELEGRAM_MB:
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=video_url,
            caption=f"🎬 {title} ({best['quality']}, {size_mb:.1f} MB)"
        )
    else:
        await update.message.reply_text(
            f"🎬 {title}\nFichier ≈ {size_mb:.1f} MB – voici le lien direct :\n{video_url}"
        )