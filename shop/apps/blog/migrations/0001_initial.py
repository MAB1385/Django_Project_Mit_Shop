# Generated by Django 3.2.11 on 2023-08-23 19:50

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article_Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان گروه')),
            ],
            options={
                'verbose_name': 'گروه',
                'verbose_name_plural': 'گروه ها',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='نام')),
                ('family', models.CharField(max_length=20, verbose_name='نام خانولدگی')),
                ('email', models.EmailField(blank=True, max_length=200, null=True, verbose_name='ایمیل')),
                ('mobile', models.CharField(max_length=11, verbose_name='شماره موبایل')),
                ('slug', models.SlugField(max_length=43)),
                ('organizational_affiliation', models.BooleanField(default=False, verbose_name='وابستگی سازمانی')),
                ('education', models.CharField(blank=True, choices=[('Diploma', 'دیپلم'), ('Associate_Degree', 'فوق دیپلم'), ('Bachelor_Degree', 'لیسانس'), ('Master_Degree', 'فوق لیسانس'), ('Doctorate', 'دکترا'), ('Specialized_Degrees', 'درجات تخصصی')], max_length=30, null=True, verbose_name='تحصیلات')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت')),
            ],
            options={
                'verbose_name': 'نویسنده',
                'verbose_name_plural': 'نویسندگان',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('slug', models.SlugField(max_length=100)),
                ('main_image', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر')),
                ('short_text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='چکیده')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='متن')),
                ('key_words', models.CharField(help_text="کلمات کلیدی را با '-' از هم جدا کنید.", max_length=1000, verbose_name='کلمات کلیدی')),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('publish_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('update_date', models.DateField(auto_now=True, verbose_name='تاریخ اخرین ویرایش')),
                ('view_number', models.PositiveSmallIntegerField(default=0, verbose_name='تعداد بازدید')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('author', models.ManyToManyField(to='blog.Author', verbose_name='نویسنده')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article_group', verbose_name='گروه')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
            },
        ),
    ]