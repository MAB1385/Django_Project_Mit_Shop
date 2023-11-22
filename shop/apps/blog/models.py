from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from utils import FileUpload


class Author(models.Model):
    file_upload = FileUpload("images", "author")
    name = models.CharField(max_length=20, verbose_name="نام")
    family = models.CharField(max_length=20, verbose_name="نام خانولدگی")
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر", null=True, blank=True
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    email = models.EmailField(
        max_length=200, verbose_name="ایمیل", null=True, blank=True
    )
    mobile = models.CharField(max_length=11, verbose_name="شماره موبایل")
    slug = models.SlugField(max_length=43)
    organizational_affiliation = models.BooleanField(
        default=False, verbose_name="وابستگی سازمانی"
    )
    EDUCATION = [
        ("Diploma", "دیپلم"),
        ("Associate_Degree", "فوق دیپلم"),
        ("Bachelor_Degree", "لیسانس"),
        ("Master_Degree", "فوق لیسانس"),
        ("Doctorate", "دکترا"),
        ("Specialized_Degrees", "درجات تخصصی"),
    ]
    education = models.CharField(
        max_length=30, verbose_name="تحصیلات", choices=EDUCATION, null=True, blank=True
    )
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"

    def __str__(self) -> str:
        return f"{self.name} {self.family}"


# todo --------------------------------------------------------------------
class Article_Group(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان گروه")
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"


# todo --------------------------------------------------------------------
class Article(models.Model):
    file_upload = FileUpload("images", "article")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.SlugField(max_length=100)
    author = models.ManyToManyField(
        Author, verbose_name="نویسنده", related_name="articles_of_authors"
    )
    group = models.ForeignKey(
        Article_Group,
        on_delete=models.CASCADE,
        verbose_name="گروه",
        related_name="articles",
    )
    main_image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر"
    )
    short_text = RichTextUploadingField(config_name="default", verbose_name="چکیده")
    text = RichTextUploadingField(config_name="default", verbose_name="متن")
    key_words = models.CharField(
        max_length=1000,
        verbose_name="کلمات کلیدی",
        help_text="کلمات کلیدی را با '-' از هم جدا کنید.",
    )
    register_date = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت")
    publish_date = models.DateField(default=timezone.now, verbose_name="تاریخ انتشار")
    update_date = models.DateField(auto_now=True, verbose_name="تاریخ اخرین ویرایش")
    view_number = models.PositiveSmallIntegerField(
        default=0, verbose_name="تعداد بازدید"
    )
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
