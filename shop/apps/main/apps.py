from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.main"
    verbose_name = "اپلیکیشن اصلی"

    #! for connect to signals
    def ready(self) -> None:
        from . import signals

        return super().ready()
