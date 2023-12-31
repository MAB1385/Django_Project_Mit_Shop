# Generated by Django 4.1.4 on 2023-05-23 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_customer_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="image",
            field=models.ImageField(
                default="images/default.png",
                upload_to=utils.FileUpload.upload_to,
                verbose_name="تصویر پروفایل",
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="coustomer",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
    ]
