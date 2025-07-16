import urllib.parse, aiohttp
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes

API_KEY  = "14960d2b4c71e3b190761233"           # ta clé lolhuman
API_URL  = "https://api.lolhuman.xyz/api/ttp"    # endpoint TTP

async def ttp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /ttp <texte>  ou  répondre à un message texte → génère un sticker PNG
    """

    # 1️⃣  Récupérer le texte
    if context.args:
        text = " ".join(context.args)
    elif update.message.reply_to_message and update.message.reply_to_message.text:
        text = update.message.reply_to_message.text
    else:
        await update.effective_message.reply_text(
            "Utilisation : /ttp <texte> (ou réponds à un message)."
        )
        return

    await update.effective_message.reply_text("🎨 Génération en cours…")

    # 2️⃣  Appel API lolhuman
    params = {"apikey": API_KEY, "text": text}
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            async with s.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text(
                        f"❌ Erreur API ({resp.status})."
                    )
                    return
                # l’API renvoie directement l’image (Content-Type: image/png)
                img_data = await resp.read()
    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erreur réseau : {e}")
        return

    # 3️⃣  Envoi du sticker
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=BytesIO(img_data),
        filename="ttp.png",
        caption="🖼️ Sticker généré par lolhuman"
    )