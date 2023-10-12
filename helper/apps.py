from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class HelperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helper'
