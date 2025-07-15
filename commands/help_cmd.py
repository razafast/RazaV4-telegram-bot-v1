from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    text = """
🧠 *Commandes disponibles :*

👋 _Commandes de base_
/start – Démarrer le bot
/help – Voir cette liste

🛡️ _Admin_
/kick – Expulser un utilisateur (admin uniquement)

🧰 _Utilitaires_
/info – Infos d’un utilisateur (nom, ID, etc.)
/ipinfo – Détails sur une IP (ville, pays…)

🎨 _Fun & Media_
/ttp – Génère un sticker texte
/lirik – Paroles d’une chanson
/ytmp4 – Télécharge une vidéo YouTube
/nsfw – Contenu NSFW (API)

⚙️ _Divers_
/ping – Vérifie la réponse du bot
/uptime – Durée de fonctionnement du bot
/ai ou /kyo – Poser une question à l’IA Kyotaka
"""
    await update.message.reply_text(text, parse_mode="Markdown")