from django.db import models

from apps.accounts.models import CustomUser
from apps.products.models import Product


class WarehouseType(models.Model):
    title = models.CharField(max_length=50, verbose_name="نوع انبار")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نوع انبار"
        verbose_name_plural = "انواع انبار"


# todo --------------------------------------------------------------------
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(
        WarehouseType,
        on_delete=models.CASCADE,
        related_name="warehouses",
        verbose_name="نوع انبار",
    )
    user_registered = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="warehouse_user_registered",
        verbose_name="کاربر ثبت کننده",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="warehouse_products",
        verbose_name="کالا",
    )
    qty = models.IntegerField(verbose_name="تعداد")
    price = models.IntegerField(verbose_name="قیمت تراکنش", null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")

    def __str__(self) -> str:
        return f"{self.warehouse_type} - {self.product}"

    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"
