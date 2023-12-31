# Generated by Django 4.1.4 on 2023-05-10 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0013_alter_brand_image_alter_product_image_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("comment_text", models.TextField(verbose_name="متن نظر")),
                (
                    "register_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج"),
                ),
                ("is_active", models.BooleanField(default=False, verbose_name="وضعیت")),
                (
                    "approving_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approving_comments_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر تایید کننده نظر",
                    ),
                ),
                (
                    "comment_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments_child",
                        to="comment_scoring_favorites.comment",
                        verbose_name="والد نظر",
                    ),
                ),
                (
                    "commenting_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر نظر دهنده",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments_product",
                        to="products.product",
                        verbose_name="کالا",
                    ),
                ),
            ],
            options={
                "verbose_name": "نظر",
                "verbose_name_plural": "نظرات",
            },
        ),
    ]
