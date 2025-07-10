from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import random

async def rps(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton("🪨 Pierre", callback_data='rock')],
        [InlineKeyboardButton("📄 Feuille", callback_data='paper')],
        [InlineKeyboardButton("✂️ Ciseaux", callback_data='scissors')],
    ]
    await update.message.reply_text("Choisis ton arme :", reply_markup=InlineKeyboardMarkup(buttons))
