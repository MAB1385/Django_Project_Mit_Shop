# Generated by Django 4.1.4 on 2023-04-07 12:31

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_alter_brand_image_alter_featurevalue_feature_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="image",
            field=models.ImageField(
                upload_to=utils.FileUpload.upload_to, verbose_name="تصویر برند"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                upload_to=utils.FileUpload.upload_to, verbose_name="تصویر کالا"
            ),
        ),
        migrations.AlterField(
            model_name="productgallery",
            name="image",
            field=models.ImageField(
                upload_to=utils.FileUpload.upload_to, verbose_name="تصویر کالا"
            ),
        ),
        migrations.AlterField(
            model_name="productgroup",
            name="image",
            field=models.ImageField(
                upload_to=utils.FileUpload.upload_to, verbose_name="تصویر گروه"
            ),
        ),
    ]
