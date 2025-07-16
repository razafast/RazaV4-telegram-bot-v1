import urllib.parse, aiohttp
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes

API_KEY   = "d90a9e986e18778b"
BASE_URL  = "https://api.xteam.xyz/ttp"

async def ttp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Génère un sticker PNG à partir d’un texte (PV, groupe, canal)."""

    # ── 1. Récupérer le texte ──────────────────────────────────────────
    if context.args:
        text = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        text = update.message.reply_to_message.text
    else:
        await update.effective_message.reply_text(
            "Utilisation : /ttp <texte> (ou réponds à un message)."
        )
        return

    # ── 2. Construire l’URL API ────────────────────────────────────────
    params = {"file": "true", "text": text, "apikey": API_KEY}
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

    # ── 3. Appeler l’API ───────────────────────────────────────────────
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text(
                        f"🚫 L’API XTeam a renvoyé {resp.status}."
                    )
                    return

                ctype = resp.headers.get("Content-Type", "")
                # a) Retour direct d’un PNG
                if "image/png" in ctype:
                    image_data = await resp.read()

                # b) Retour JSON → on récupère l’URL puis on retélécharge l’image
                else:
                    data = await resp.json()
                    file_url = (
                        data.get("result", {}).get("file")           # certain cas
                        or data.get("result", {}).get("url")         # autre cas
                        or data.get("url")                           # fallback
                    )
                    if not file_url:
                        await update.effective_message.reply_text("🚫 Réponse API invalide.")
                        return
                    async with s.get(file_url) as img_resp:
                        if img_resp.status != 200:
                            await update.effective_message.reply_text("🚫 Impossible de récupérer le fichier.")
                            return
                        image_data = await img_resp.read()

    except aiohttp.ClientError as e:
        await update.effective_message.reply_text(f"🚫 Erreur réseau : {e}")
        return

    # ── 4. Envoyer la photo ────────────────────────────────────────────
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=BytesIO(image_data),
        filename="ttp.png",
        caption="🖼️ Sticker généré par XTeam"
    )