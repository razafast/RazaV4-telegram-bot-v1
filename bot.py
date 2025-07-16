import logging import time from telegram import Update from telegram.ext import ( ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, )

=== Command modules ===

from commands.kick import kick from commands.unban import unban from commands.help_cmd import help_command from commands.info import info from commands.ttp import ttp from commands.lirik import lirik from commands.ass import ass from commands.boobs import boobs from commands.hboobs import hboobs  # NEW from commands.ipinfo import ipinfo

=== Misc commands ===

from commands.ping import ping from commands.uptime import uptime from commands.nsfw import nsfw from commands.ai_kyo import ai_kyo

TOKEN = "8146852566:AAHf8Jkrd124pWD1N6G9AeOKxtGIi3gvouA"

logging.basicConfig( format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): """Message de bienvenue.""" await update.message.reply_text( "🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes." )

def main() -> None: app = ApplicationBuilder().token(TOKEN).build()

app.bot_data["start_time"] = time.time()

# === Commandes de base ===
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# === Admin ===
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("unban", unban))

# === Utilitaires ===
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("ipinfo", ipinfo))

# === Fun / Media ===
app.add_handler(CommandHandler("ttp", ttp))
app.add_handler(CommandHandler("lirik", lirik))
app.add_handler(CommandHandler("ass", ass))
app.add_handler(CommandHandler("boobs", boobs))
app.add_handler(CommandHandler("hboobs", hboobs))  # NEW

# === Divers ===
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("uptime", uptime))
app.add_handler(CommandHandler("nsfw", nsfw))
app.add_handler(CommandHandler(["ai", "kyo"], ai_kyo))

# === Inline callbacks (if any) ===
# app.add_handler(CallbackQueryHandler(handle_callback))  # optional

logging.info("✅ Bot lancé et prêt à répondre ✨")
app.run_polling()

if name == "main": main()

