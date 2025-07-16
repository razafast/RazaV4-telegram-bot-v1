import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "http://ip-api.com/json/{}"

def bool_emoji(value):
    return "✅ Oui" if value else "❌ Non"

async def ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text("Utilisation : /ipinfo <adresse-IP>")
        return

    ip = context.args[0]
    url = API_URL.format(ip)

    await update.effective_message.reply_text("🌐 Recherche en cours…")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text(f"❌ Erreur API ({resp.status}).")
                    return
                data = await resp.json()
    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erreur réseau : {e}")
        return

    if data.get("status") != "success":
        await update.effective_message.reply_text("❌ IP invalide ou non trouvée.")
        return

    ip        = data.get("query", "—")
    country   = data.get("country", "—")
    region    = data.get("regionName", "—")
    city      = data.get("city", "—")
    continent = data.get("continent", "—")
    lat       = data.get("lat", None)
    lon       = data.get("lon", None)
    timezone  = data.get("timezone", "—")
    offset    = data.get("offset", 0)
    isp       = data.get("isp", "—")
    org       = data.get("org", "—")
    asn       = data.get("as", "—")

    mobile    = bool_emoji(data.get("mobile", False))
    proxy     = bool_emoji(data.get("proxy", False))
    hosting   = bool_emoji(data.get("hosting", False))

    # Lien vers carte Google Maps
    maps_link = f"https://maps.google.com/?q={lat},{lon}" if lat and lon else "—"

    txt = (
        f"🌐 <b>IP :</b> <code>{ip}</code>\n"
        f"🏳️ <b>Pays :</b> {country}\n"
        f"📍 <b>Région / Ville :</b> {region}, {city}\n"
        f"🌍 <b>Continent :</b> {continent}\n"
        f"🛰️ <b>Réseau :</b> {asn}\n"
        f"🏢 <b>FAI :</b> {isp}\n"
        f"🏷️ <b>Organisation :</b> {org}\n"
        f"📡 <b>Coordonnées :</b> {lat}, {lon}\n"
        f"🗺️ <b>Carte :</b> <a href='{maps_link}'>Voir sur Google Maps</a>\n"
        f"⏰ <b>Fuseau :</b> {timezone} (UTC{offset//3600:+d})\n"
        f"📶 <b>Mobile :</b> {mobile} | <b>Proxy :</b> {proxy} | <b>Hosting :</b> {hosting}"
    )

    await update.effective_message.reply_html(txt, disable_web_page_preview=False)