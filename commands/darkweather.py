import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = "4a9adedce78abeea7923181e79926e29"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

DARK_DESCRIPTIONS = {
    "Clear": "Le ciel clair expose la nuit froide et sans étoiles.",
    "Clouds": "Des nuages sombres enveloppent le monde d'un voile de mystère.",
    "Rain": "La pluie sanglante lave les ruelles désertes.",
    "Drizzle": "Une bruine funèbre tombe doucement, comme des larmes invisibles.",
    "Thunderstorm": "Le tonnerre gronde, écho des cauchemars nocturnes.",
    "Snow": "La neige froide recouvre les âmes errantes d’un linceul blanc.",
    "Mist": "Le brouillard épais dissimule les secrets les plus sombres.",
    "Fog": "Le brouillard obscurcit les vérités enfouies dans l’ombre."
}

async def darkweather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /darkweather <ville>")
        return

    city = " ".join(context.args)
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "fr"}

    await update.message.reply_text(f"🔮 Invocation des ténèbres météo pour {city}...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Erreur API météo : {resp.status}")
                    return
                data = await resp.json()

        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        desc = DARK_DESCRIPTIONS.get(weather, "Le ciel pleure ses sombres secrets.")

        msg = (
            f"🌑 *Météo Sombre pour {city.title()}*\n"
            f"Condition : {weather}\n"
            f"Température : {temp}°C\n\n"
            f"📜 {desc}"
        )

        await update.message.reply_markdown(msg)

    except Exception as e:
        await update.message.reply_text(f"Erreur réseau : {e}")
