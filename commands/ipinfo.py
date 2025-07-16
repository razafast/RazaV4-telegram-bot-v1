import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "http://ip-api.com/json/{}"

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

    country   = data.get("country", "—")
    region    = data.get("regionName", "—")
    city      = data.get("city", "—")
    timezone  = data.get("timezone", "—")
    isp       = data.get("isp", "—")
    org       = data.get("org", "—")

    txt = (
        f"🌐 <b>IP :</b> <code>{ip}</code>\n"
        f"🏳️ <b>Pays :</b> {country}\n"
        f"📍 <b>Région / Ville :</b> {region}, {city}\n"
        f"⏰ <b>Fuseau :</b> {timezone}\n"
        f"🏢 <b>FAI :</b> {isp}\n"
        f"🏷️ <b>Organisation :</b> {org}"
    )
    await update.effective_message.reply_html(txt)