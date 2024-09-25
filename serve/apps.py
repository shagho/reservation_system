from django.apps import AppConfig


class ServeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serve'
    verbose_name = 'مدیریت رزرواسیون'

    def ready(self):
        import serve.signals
    