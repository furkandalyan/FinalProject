
from django.apps import AppConfig

class YonetimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yonetim'

    def ready(self):
        print("💡 apps.py: ready() çalıştı")  # test satırı
        from .auto_checker_embed import start_background_checker
        start_background_checker()

