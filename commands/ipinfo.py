# commands/ipinfo.py
import urllib.parse, aiohttp
from telegram import Update
from telegram.ext import ContextTypes

# Clé fournie pour l’API XTeam
API_KEY = "d90a9e986e18778b"

async def ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /ipinfo <adresse-IP>
    Renvoie : pays, région, ville, FAI, fuseau horaire, organisation.
    """

    if not context.args:
        await update.message.reply_text("Utilisation : /ipinfo <adresse-IP>")
        return

    ip = context.args[0]

    # ── appel API XTeam ───────────────────────────────────────────────
    url = (
        "https://api.xteam.xyz/cekip?"
        + urllib.parse.urlencode({"ip": ip, "apikey": API_KEY})
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await update.message.reply_text("❌ Impossible d’obtenir les infos.")
                return
            raw = await resp.json()

    # L’API renvoie soit directement les champs, soit sous « result »
    data = raw.get("result", raw)

    # ── extraction avec valeurs par défaut ───────────────────────────
    country   = data.get("country", "—")
    region    = data.get("regionName", data.get("region", "—"))
    city      = data.get("city", "—")
    timezone  = data.get("timezone", "—")
    isp       = data.get("isp", "—")
    org       = data.get("org", data.get("organization", "—"))

    msg = (
        f"🌐 <b>IP :</b> <code>{ip}</code>\n"
        f"🏳️ <b>Pays :</b> {country}\n"
        f"📍 <b>Région / Ville :</b> {region}, {city}\n"
        f"⏰ <b>Fuseau horaire :</b> {timezone}\n"
        f"🏢 <b>FAI :</b> {isp}\n"
        f"🏷️ <b>Organisation :</b> {org}"
    )

    await update.message.reply_html(msg)