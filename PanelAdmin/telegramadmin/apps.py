from django.apps import AppConfig


class TelegramadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegramadmin'
    verbose_name = "مدیریت ربات"
    def ready(self):
        import telegramadmin.signals
