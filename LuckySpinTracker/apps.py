from django.apps import AppConfig


class LuckyspintrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LuckySpinTracker'

    def ready(self):
        import LuckySpinTracker.signals