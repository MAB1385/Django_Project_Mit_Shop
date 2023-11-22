from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.products.models import Product


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True, verbose_name="کد کوپن")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ انقضاء")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
    )
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپن ها"

    def __str__(self) -> str:
        return self.coupon_code


# todo --------------------------------------------------------------------
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name="عنوان سبد تخفیف")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ انقضاء")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
    )
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = "سبد تخفیف"
        verbose_name_plural = "سبدهای تخفیف"

    def __str__(self) -> str:
        return self.discount_title


# todo --------------------------------------------------------------------
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(
        DiscountBasket,
        on_delete=models.CASCADE,
        verbose_name="سبد خرید",
        related_name="discount_basket_details1",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="کالا",
        related_name="discount_basket_details2",
    )

    class Meta:
        verbose_name = "کالا سبد تخفیف"
        verbose_name_plural = "کالاهای سبد تخفیف"
