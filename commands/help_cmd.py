from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🤖 Kyo dark ia", callback_data="ai")],
        [InlineKeyboardButton("🧠 Ai tools", callback_data="ai_tools"),
         InlineKeyboardButton("🌼 Matches organisator", callback_data="matches")],
        [InlineKeyboardButton("📲 Éditeur vid", callback_data="editeur_vid"),
         InlineKeyboardButton("💥 KitHack", callback_data="kithack")],
        [InlineKeyboardButton("❌ VMOS Pro", callback_data="vmos"),
         InlineKeyboardButton("🤖 Smart Auto", callback_data="auto")],
        [InlineKeyboardButton("🛡️ Kick", callback_data="kick"),
         InlineKeyboardButton("♻️ Unban", callback_data="unban")],
        [InlineKeyboardButton("📍 IP Info", callback_data="ipinfo"),
         InlineKeyboardButton("📵 IP Masquer", callback_data="ip_masquer")],
        [InlineKeyboardButton("🎵 Lirik", callback_data="lirik"),
         InlineKeyboardButton("📹 YT MP4", callback_data="ytmp4")],
        [InlineKeyboardButton("🔞 NSFW", callback_data="nsfw"),
         InlineKeyboardButton("🔞 Boobs", callback_data="boobs")],  # ← Ajout ici
        [InlineKeyboardButton("📊 Ping", callback_data="ping"),
         InlineKeyboardButton("⏱️ Uptime", callback_data="uptime")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧠 *Commandes disponibles :*\nChoisis une commande ci-dessous 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )