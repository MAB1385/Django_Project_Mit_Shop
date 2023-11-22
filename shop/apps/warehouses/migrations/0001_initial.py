# Generated by Django 4.1.4 on 2023-05-01 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0012_alter_brand_image_alter_product_image_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WarehouseType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="")),
            ],
            options={
                "verbose_name": "",
                "verbose_name_plural": "",
            },
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qty", models.IntegerField(verbose_name="")),
                ("price", models.IntegerField(blank=True, null=True, verbose_name="")),
                (
                    "register_date",
                    models.DateTimeField(auto_now_add=True, verbose_name=""),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="warehouse_products",
                        to="products.product",
                        verbose_name="",
                    ),
                ),
                (
                    "user_registered",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="warehouse_user_registered",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="",
                    ),
                ),
                (
                    "warehouse_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="warehouses",
                        to="warehouses.warehousetype",
                        verbose_name="",
                    ),
                ),
            ],
            options={
                "verbose_name": "",
                "verbose_name_plural": "",
            },
        ),
    ]