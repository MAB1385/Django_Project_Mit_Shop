from uuid import uuid4

from django.db import models
from django.utils import timezone
from utils import price_by_delivery_tax

from apps.accounts.models import Customer, CustomUser
from apps.products.models import Product, ProductColor


class PaymentType(models.Model):
    payment_title = models.CharField(max_length=50, verbose_name="عنوان پرداخت")

    def __str__(self) -> str:
        return self.payment_title

    class Meta:
        verbose_name = "نوع روش پرداخت"
        verbose_name_plural = "انواع روش پرداخت"


# todo --------------------------------------------------------------------
class OrderState(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "وضعیت سفارش"
        verbose_name_plural = "وضعیت های سفارش"


# todo --------------------------------------------------------------------
class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="مشتری"
    )
    register_date = models.DateField(default=timezone.now, verbose_name="تاریخ درج")
    update_date = models.DateField(auto_now=True, verbose_name="تاریخ آخرین ویرایش")
    is_finaly = models.BooleanField(default=False, verbose_name="نهایی شده")
    order_code = models.UUIDField(
        unique=True, editable=False, default=uuid4, verbose_name="کد سفارش"
    )
    discount = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="مقدار تخفیف سفارش"
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    payment_type = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        verbose_name="روش پرداخت",
        related_name="payment_types",
    )
    order_state = models.ForeignKey(
        OrderState,
        on_delete=models.CASCADE,
        verbose_name="وضعیت سفارش",
        related_name="order_state",
        null=True,
        blank=True,
    )

    def get_order_total_price(self):
        sum_ = 0
        for item in self.orders_details.all():
            sum_ += item.total_price
        order_finaly_price, delivery, tax = price_by_delivery_tax(sum_, self.discount)
        return order_finaly_price * 10

    def __str__(self) -> str:
        return f"{self.customer}\t{self.id}\t{self.is_finaly}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"


# todo --------------------------------------------------------------------
class ShopCart(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="orders_details",
        verbose_name="سفارش",
        null=True,
        blank=True,
        default=None,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_shopcart",
        verbose_name="کاربر",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_shopcart",
        verbose_name="کالا",
    )
    product_color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name="product_color_shopcart",
        null=True,
        blank=True,
        verbose_name="رنگ",
    )
    qty = models.IntegerField(default=0, verbose_name="تعداد")
    total_price = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="قیمت کل"
    )

    def __str__(self) -> str:
        if self.product_color:
            return (
                f"{self.user.name} - {self.product.name} - {self.product_color.color}"
            )
        else:
            return f"{self.user.name} - {self.product.name}"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید ها"
