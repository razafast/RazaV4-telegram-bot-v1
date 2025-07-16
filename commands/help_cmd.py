from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📌 Start", callback_data="start"),
         InlineKeyboardButton("ℹ️ Help", callback_data="help")],

        [InlineKeyboardButton("🛡️ Kick", callback_data="kick"),
         InlineKeyboardButton("♻️ Unban", callback_data="unban")],

        [InlineKeyboardButton("📍 IP Info", callback_data="ipinfo"),
         InlineKeyboardButton("🧠 Info", callback_data="info")],

        [InlineKeyboardButton("🎨 TTP", callback_data="ttp"),
         InlineKeyboardButton("🎵 Lirik", callback_data="lirik")],

        [InlineKeyboardButton("📹 YT MP4", callback_data="ytmp4"),
         InlineKeyboardButton("🔞 Boobs", callback_data="boobs")],

        [InlineKeyboardButton("🔞 NSFW", callback_data="nsfw"),
         InlineKeyboardButton("🤖 IA Kyotaka", callback_data="ai")],

        [InlineKeyboardButton("📊 Ping", callback_data="ping"),
         InlineKeyboardButton("⏱️ Uptime", callback_data="uptime")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧠 *Commandes disponibles :*\nAppuie sur un bouton ci-dessous 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )