from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = "اپلیکیشن مدیریت کالا"

    #! for connect to signals
    def ready(self) -> None:
        from . import signals

        return super().ready()
