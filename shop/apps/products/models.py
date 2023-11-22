# from ckeditor.fields import RichTextField
from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.db import models
from django.db.models import Avg, Max, Min, Q, Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from middlewares.middlewares import RequestMiddleware
from utils import FileUpload


class Brand(models.Model):
    file_upload = FileUpload("images", "brand")
    title = models.CharField(max_length=100, verbose_name="نام برند")
    slug = models.SlugField(max_length=200, null=True)
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر برند"
    )
    description = RichTextUploadingField(
        config_name="default", blank=True, null=True, verbose_name="توضیحات برند"
    )

    def get_absolute_url(self):
        return reverse("products:brand_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"


# todo --------------------------------------------------------------------
class ProductGroup(models.Model):
    file_upload = FileUpload("images", "product_group")
    title = models.CharField(max_length=100, verbose_name="عنوان گروه")
    slug = models.SlugField(max_length=200, null=True)
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر گروه"
    )
    description = RichTextUploadingField(
        config_name="default", blank=True, null=True, verbose_name="توضیحات گروه"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال / غیر فعال")
    group_parent = models.ForeignKey(
        "ProductGroup",  #! If the ForeignKey of a model is equal to that model, we should put it in "".
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="گروه والد",
        related_name="groups",
    )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="تاریخ انتشار"
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def get_absolute_url(self):
        return reverse("products:product_by_group", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "گروه کالا"
        verbose_name_plural = "گروه های کالا"


# todo --------------------------------------------------------------------
class Feature(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام ویژگی")
    product_group = models.ManyToManyField(
        ProductGroup, verbose_name="گروه کالا", related_name="features_of_groups"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"


# todo --------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=500, verbose_name="نام کالا")
    slug = models.SlugField(max_length=200, null=True)
    summery_description = RichTextUploadingField(
        config_name="default", blank=True, null=True, verbose_name="توضیحات کوتاه کالا"
    )
    description = RichTextUploadingField(
        config_name="default", blank=True, null=True, verbose_name="توضیحات کالا"
    )
    file_upload = FileUpload("images", "product_group")
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر کالا"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت کالا")
    product_group = models.ManyToManyField(
        ProductGroup, verbose_name="گروه کالا", related_name="products_of_groups"
    )
    features = models.ManyToManyField(Feature, through="ProductFeature")
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name="برند کالا",
        related_name="brands",
        null=True,
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال / غیر فعال")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="تاریخ انتشار"
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def get_price_by_discount(self):
        list_discount = []
        for dbd in self.discount_basket_details2.all():
            if (
                dbd.discount_basket.is_active
                and dbd.discount_basket.start_date <= datetime.now()
                and datetime.now() <= dbd.discount_basket.end_date
            ):
                list_discount.append(dbd.discount_basket.discount)
        discount = 0
        if len(list_discount) > 0:
            discount = max(list_discount)
        return int(self.price - (self.price * discount / 100))

    def get_number_in_warehouse(self):
        sum1 = self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum("qty"))
        sum2 = self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum("qty"))
        input = 0
        if sum1["qty__sum"] != None:
            input = sum1["qty__sum"]
        output = 0
        if sum2["qty__sum"] != None:
            output = sum2["qty__sum"]
        return input - output

    def get_number_in_my_order(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        product_shopcarts = self.product_shopcart.filter(
            Q(user=request.user) & Q(order=None)
        ).aggregate(Sum("qty"))
        count = 0
        if product_shopcarts["qty__sum"] != None:
            count = product_shopcarts["qty__sum"]
        return count

    def get_average_score(self):
        avg_score = self.product_scoring.all().aggregate(Avg("score"))["score__avg"]
        if avg_score == None:
            avg_score = 0
        return avg_score

    def get_user_score(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.product_scoring.filter(scoring_user=request.user)
        if user_score.count() > 0:
            score = user_score[0].score
        return score

    def get_user_favorite(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        flag = self.product_favorite.filter(favorite_user=request.user).exists()
        return flag

    def get_product_groups(self):
        groups_set = set({})
        for group in self.product_group.all():
            groups_set.add(group.id)
        return groups_set

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا ها"


# todo --------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100, verbose_name="عنوان مقدار")
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="ویژگی",
        related_name="feature_values",
    )

    def __str__(self) -> str:
        return f"{self.id} {self.value_title}"

    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی"


# todo --------------------------------------------------------------------
class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="کالا",
        related_name="product_features",
    )
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="ویژگی")
    value = models.CharField(max_length=200, verbose_name="مقدار ویژگی کالا")
    filter_value = models.ForeignKey(
        FeatureValue,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="کلید مقدار",
    )

    def __str__(self):
        return f"{self.product} _ {self.feature} : {self.value}"

    class Meta:
        verbose_name = "ویژگی کالا"
        verbose_name_plural = "ویژگی های کالا"


# todo --------------------------------------------------------------------
class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="کالا",
        related_name="product_gallery",
    )
    file_upload = FileUpload("images", "product_gallery")
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر کالا"
    )

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"


# todo --------------------------------------------------------------------
class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="کالا",
        related_name="product_colors",
    )
    name = models.CharField(max_length=500, verbose_name="نام رنگ")
    color = ColorField(max_length=10, verbose_name="رنگ")
    value_added = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="ارزش افزوده"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"


#! =========================================== signals ===========================================
# ? way 1:
# def fun(sender, **kwargs):
#    print("hello")
# post_delete.connect(receiver=fun, sender=Product)

# ? way 2:
# @receiver(post_delete,sender=Product)
# def fun(sender, **kwargs):
#    print("hello")
