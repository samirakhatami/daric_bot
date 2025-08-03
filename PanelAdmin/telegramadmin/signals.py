from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Analysis, AnalysisMember, Bot
import requests
import jdatetime
import os
import mimetypes
from django.conf import settings

Bots = Bot.objects.filter(id = 17)
for bot in Bots:
    Bot_Token = bot.token


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{Bot_Token}/sendMessage"
    data = {
        "chat_id" : chat_id,
        "text" : text,
        "parse_mode" : "HTML"
    }
    requests.post(url, data=data)

def send_document(chat_id, file_path, caption): 
    url = f"https://api.telegram.org/bot{Bot_Token}/sendDocument"
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': chat_id, "caption": caption}
        requests.post(url, data=data, files=files)

def send_photo(chat_id, file_path, caption):
    url = f"https://api.telegram.org/bot{Bot_Token}/sendPhoto"
    with open(file_path, 'rb') as f:
        files = {'photo': f}
        data = {"chat_id": chat_id, "caption": caption}
        requests.post(url, data=data, files=files)


@receiver(post_save, sender = Analysis)
def send_analysis_to_users(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.state != 1:
        return
    MEDIA_ROOT = settings.MEDIA_ROOT
    file_path = os.path.join(MEDIA_ROOT, instance.file)
    today_jalali = jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')
    text = f"<b>{instance.title}</b>\n\n{instance.text}\n\nتاریخ: {today_jalali}"

    file_path = os.path.join(MEDIA_ROOT,instance.file) if instance.file else None
    has_file = file_path and os.path.isfile(file_path)
    for user in AnalysisMember.objects.filter(send_analysis= 1):
        try:
            if has_file:
                mim_type, _ = mimetypes.guess_type(file_path)
                if mim_type and mim_type.startswith("image/"):
                    send_photo(user.chat_id, file_path, text)
                else:
                    send_document(user.chat_id, file_path, text)
            else:
                send_telegram_message(user.chat_id, text)
        except Exception as e:
            print("❌❌❌error:", e)
        



