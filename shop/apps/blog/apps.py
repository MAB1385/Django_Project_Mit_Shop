from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog"
    verbose_name = "اپلیکیشن مدیریت مقالات "

    #! for connect to signals
    def ready(self) -> None:
        from . import signals

        return super().ready()
