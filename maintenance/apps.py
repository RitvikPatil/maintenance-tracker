from django.apps import AppConfig

class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance'

    def ready(self):
        # Import signals to register them
        import maintenance.signals  # noqa
