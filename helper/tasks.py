import django_rq
from datetime import timedelta
from datetime import datetime
import requests
from django_rq import job
import pytz 
import schedule
import time
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

import logging
logger = logging.getLogger(__name__)

FCM_API_URL = 'https://fcm.googleapis.com/fcm/send'
FCM_API_KEY = 'AAAAx4VMzgQ:APA91bEn1hLMiCfhE7b3-WmrKl7yXauJGXhHM2LHQhjN_HO1ftldEHIjGJEaFlfp7Q48kKwcuvsgLjbZ7sLujoJKuVhLQpI0yZX3AINWlzrzU7XZDmw1fjjGevlMhLGO3u4ouObuM3au'

def send_notifications():
    
    from account.models import usercore
    from rest_framework.authtoken.models import Token

    logger.info("send_notifications taskı başladı.")
    
    usercores = usercore.objects.all()  # `usercore` Django modelinizin adıdır, değiştirilebilir
    
    for user in usercores:
            try:
                fbm_token = user.firebase_messaging_token  # FBM token'ını usercore modelinden alın
                if not fbm_token:
                    logger.warning(f"{user.username} için FBM token bulunamadı.")
                    continue

                title = 'Selam'
                message = f'Nasılsın {user.username}'

                headers = {
                    'Authorization': f'key={FCM_API_KEY}',
                    'Content-Type': 'application/json',
                }
                data = {
                    'to': fbm_token,
                    'notification': {
                        'title': title,
                        'body': message
                    },
                        'data': {
        'extra_info': 'some_extra_info'
                 }
                    
                }

                response = requests.post(FCM_API_URL, headers=headers, json=data)


                if response.status_code == 200:
                    logger.info(f"{user.username} için bildirim gönderildi. Token: {fbm_token } data: {data}")
                else:
                    logger.warning(f"{user.username} için bildirim gönderilemedi, sebep: {response.text}")

            except Exception as e:
                logger.error(f"{user.username} için bildirim gönderilirken hata: {e}")
                continue