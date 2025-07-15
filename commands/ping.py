from telegram import Update
from telegram.ext import CallbackContext
import time

async def ping(update: Update, context: CallbackContext):
    start_time = time.time()
    message = await update.message.reply_text("Ping...")
    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)
    await message.edit_text(f"Pong ! 🏓\nLatence : {latency_ms} ms")