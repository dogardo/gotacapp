import os
from datetime import datetime
from pytz import timezone
from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler
from helper.tasks import send_notifications  # Fonksiyonunuzun yolu

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gotac.settings')

def my_scheduled_job():
    send_notifications()

scheduler = BackgroundScheduler(timezone='Europe/Istanbul')

# Şu anki zamanı al
istanbul = timezone('Europe/Istanbul')
current_time = datetime.now(istanbul)

# Görevi şu anki zamanla başlat ve her 10 saniyede bir tekrarla
scheduler.add_job(my_scheduled_job, 'interval', seconds=10, start_date=current_time)
scheduler.start()

application = get_wsgi_application()