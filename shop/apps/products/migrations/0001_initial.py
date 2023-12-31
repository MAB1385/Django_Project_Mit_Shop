# Generated by Django 4.1.4 on 2023-02-17 17:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("title", models.CharField(max_length=100, verbose_name="نام برند")),
                ("slug", models.SlugField(max_length=200, null=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=utils.FileUpload.upload_to, verbose_name="تصویر برند"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="توضیحات برند"
                    ),
                ),
            ],
            options={
                "verbose_name": "برند",
                "verbose_name_plural": "برند ها",
            },
        ),
        migrations.CreateModel(
            name="Feature",
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
                ("name", models.CharField(max_length=100, verbose_name="نام ویژگی")),
            ],
            options={
                "verbose_name": "ویژگی",
                "verbose_name_plural": "ویژگی ها",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=500, verbose_name="نام کالا")),
                ("slug", models.SlugField(max_length=200, null=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="توضیحات کالا"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=utils.FileUpload.upload_to, verbose_name="تصویر کالا"
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(default=0, verbose_name="قیمت کالا"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="فعال / غیر فعال"),
                ),
                (
                    "register_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج"),
                ),
                (
                    "published_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="تاریخ انتشار"
                    ),
                ),
                (
                    "update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brands",
                        to="products.brand",
                        verbose_name="برند کالا",
                    ),
                ),
            ],
            options={
                "verbose_name": "کالا",
                "verbose_name_plural": "کالا ها",
            },
        ),
        migrations.CreateModel(
            name="ProductGroup",
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
                ("title", models.CharField(max_length=100, verbose_name="عنوان گروه")),
                ("slug", models.SlugField(max_length=200, null=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=utils.FileUpload.upload_to, verbose_name="تصویر گروه"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="توضیحات گروه"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="فعال / غیر فعال"),
                ),
                (
                    "register_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج"),
                ),
                (
                    "published_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="تاریخ انتشار"
                    ),
                ),
                (
                    "update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
                    ),
                ),
                (
                    "group_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="groups",
                        to="products.productgroup",
                        verbose_name="گروه والد",
                    ),
                ),
            ],
            options={
                "verbose_name": "گروه کالا",
                "verbose_name_plural": "گروه های کالا",
            },
        ),
        migrations.CreateModel(
            name="ProductGallery",
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
                (
                    "image",
                    models.ImageField(
                        upload_to=utils.FileUpload.upload_to, verbose_name="تصویر کالا"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="کالا",
                    ),
                ),
            ],
            options={
                "verbose_name": "تصویر",
                "verbose_name_plural": "تصاویر",
            },
        ),
        migrations.CreateModel(
            name="ProductFeature",
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
                (
                    "value",
                    models.CharField(max_length=200, verbose_name="مقدار ویژگی کالا"),
                ),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.feature",
                        verbose_name="ویژگی",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="کالا",
                    ),
                ),
            ],
            options={
                "verbose_name": "ویژگی کالا",
                "verbose_name_plural": "ویژگی های کالا",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="features",
            field=models.ManyToManyField(
                through="products.ProductFeature", to="products.feature"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="product_group",
            field=models.ManyToManyField(
                related_name="products_of_groups",
                to="products.productgroup",
                verbose_name="گروه کالا",
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="product_group",
            field=models.ManyToManyField(
                related_name="features_of_groups",
                to="products.productgroup",
                verbose_name="گروه کالا",
            ),
        ),
    ]
