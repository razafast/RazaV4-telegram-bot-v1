import tempfile
import os
from pytube import YouTube
from telegram import Update
from telegram.ext import ContextTypes

async def ytmp4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /ytmp4 <lien YouTube>")
        return

    url = context.args[0]
    await update.message.reply_text("⏳ Téléchargement en cours...")

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last()
        if not stream:
            raise Exception("Aucun flux mp4 trouvé.")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        stream.download(output_path=os.path.dirname(tmp.name), filename=os.path.basename(tmp.name))
        tmp.close()
        await update.message.reply_video(open(tmp.name, 'rb'), caption=yt.title)
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)