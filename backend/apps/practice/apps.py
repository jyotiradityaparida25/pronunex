from django.apps import AppConfig


class PracticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.practice'
    verbose_name = 'Practice Sessions'
    
    def ready(self):
        # Import signals to register handlers
        import apps.practice.signals
