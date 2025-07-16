from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import requests

API_KEY = "14960d2b4c71e3b190761233"
API_URL = "https://api.lolhuman.xyz/api/nsfw/boobs"

def boobs(update: Update, context: CallbackContext) -> None:
    params = {"apikey": API_KEY}
    res = requests.get(API_URL, params=params)
    if res.status_code == 200:
        data = res.json()
        image_url = data.get("result")
        if image_url:
            update.message.reply_photo(photo=image_url, caption="Voici tes boobs 😏")
        else:
            update.message.reply_text("Pas d'image retournée par l'API 😕")
    else:
        update.message.reply_text("Erreur lors de la requête à l'API.")

boobs_handler = CommandHandler("boobs", boobs)
dispatcher.add_handler(boobs_handler)