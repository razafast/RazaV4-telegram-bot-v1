from telegram import Update
from telegram.ext import CallbackContext
import time

async def uptime(update: Update, context: CallbackContext):
    current_time = time.time()
    uptime_seconds = int(current_time - context.bot_data.get("start_time", current_time))

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    await update.message.reply_text(
        f"⏱️ Uptime du bot :\n"
        f"{days}j {hours}h {minutes}m {seconds}s"
    )