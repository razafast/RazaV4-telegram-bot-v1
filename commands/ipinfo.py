import urllib.parse, aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY  = "14960d2b4c71e3b190761233"            # ta clé lolhuman
API_URL  = "https://api.lolhuman.xyz/api/iplookup"

async def ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /ipinfo <adresse-IP>
    Renvoie pays, région, ville, FAI, org, fuseau horaire…
    """

    if not context.args:
        await update.effective_message.reply_text("Utilisation : /ipinfo <adresse-IP>")
        return

    ip = context.args[0]
    params = {"apikey": API_KEY, "query": ip}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    await update.effective_message.reply_text("🌐 Recherche en cours…")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text(f"❌ Erreur API ({resp.status}).")
                    return
                raw = await resp.json()
    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erreur réseau : {e}")
        return

    data = raw.get("result", raw)

    country   = data.get("country", "—")
    region    = data.get("regionName", data.get("region", "—"))
    city      = data.get("city", "—")
    timezone  = data.get("timezone", "—")
    isp       = data.get("isp", "—")
    org       = data.get("org", data.get("organization", "—"))

    txt = (
        f"🌐 <b>IP :</b> <code>{ip}</code>\n"
        f"🏳️ <b>Pays :</b> {country}\n"
        f"📍 <b>Région / Ville :</b> {region}, {city}\n"
        f"⏰ <b>Fuseau :</b> {timezone}\n"
        f"🏢 <b>FAI :</b> {isp}\n"
        f"🏷️ <b>Organisation :</b> {org}"
    )
    await update.effective_message.reply_html(txt)