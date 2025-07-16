from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    help_text = """
🧠 *Commandes disponibles :*

/start  – Démarrer le bot
/help   – Afficher cette aide

👮 Admin
/kick   – Expulser un membre
/unban  – Débannir un utilisateur

📡 Réseau
/ipinfo <ip>      – Infos sur une IP

🎵 Média
/lirik <titre>    – Paroles de chanson
/ttp <texte>      – Sticker texte

🔞 NSFW
/nsfw             – Menu NSFW
/ass              – Image NSFW ass 🍑
/boobs            – Image NSFW aléatoire
/hboobs           – Image NSFW hboobs

🎨 Dark & Fun
/darkgen <prompt>     – Génère une image dark
/darkweather <ville>  – Météo dark

📚 Définitions
/defdark <mot>        – Définitions dark automatiques

⚙️ Divers
/ping                – Vérifie la latence
/uptime              – Durée de fonctionnement
/info                – Infos sur le bot
/ai <question>        – IA Kyotaka
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")
