from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.accounts.models import CustomUser
from apps.products.models import Product


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments_product",
        verbose_name="کالا",
    )
    commenting_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments_user",
        verbose_name="کاربر نظر دهنده",
    )
    approving_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="approving_comments_user",
        verbose_name="کاربر تایید کننده نظر",
        null=True,
        blank=True,
    )
    comment_text = models.TextField(verbose_name="متن نظر")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    comment_parent = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="والد نظر",
        related_name="comments_child",
    )

    def __str__(self) -> str:
        return f"{self.product} - {self.commenting_user}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


# todo --------------------------------------------------------------------
class Scoring(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_scoring",
        verbose_name="کالا",
    )
    scoring_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_scoring",
        verbose_name="کاربر امتیاز دهنده",
    )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="امتیاز"
    )

    def __str__(self) -> str:
        return f"{self.product} - {self.scoring_user}"

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازات"


# todo --------------------------------------------------------------------
class Favorite(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_favorite",
        verbose_name="کالا",
    )
    favorite_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_favorite",
        verbose_name="کاربر امتیاز دهنده",
    )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")

    def __str__(self) -> str:
        return f"{self.product} - {self.favorite_user}"

    class Meta:
        verbose_name = "علاقه"
        verbose_name_plural = "علایق"
