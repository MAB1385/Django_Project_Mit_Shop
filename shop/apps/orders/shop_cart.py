from django.db.models import Count, Q

from apps.products.models import Product, ProductColor

from .models import ShopCart as shop_cart_model


class ShopCart:
    def __init__(self, request) -> None:
        self.user = request.user
        self.count_shop_cart()
        self.shop_cart_dict = {
            item.product.id: item.qty
            for item in shop_cart_model.objects.filter(
                Q(user=self.user) & Q(order=None)
            )
        }

    def count_shop_cart(self):
        self.count = shop_cart_model.objects.filter(
            Q(user=self.user) & Q(order=None)
        ).count()

    def add_to_shop_cart(self, product, qty, color):
        try:
            shop_cart = shop_cart_model.objects.get(
                Q(user=self.user)
                & Q(product=product)
                & Q(product_color=color)
                & Q(order=None)
            )
            shop_cart.qty += qty
            if shop_cart.qty > shop_cart.product.get_number_in_warehouse():
                shop_cart.qty = shop_cart.product.get_number_in_warehouse()
            total_price = shop_cart.qty * shop_cart.product.get_price_by_discount()
            if shop_cart.product_color != None:
                total_price += shop_cart.product_color.value_added * shop_cart.qty
            shop_cart.total_price = total_price
        except shop_cart_model.DoesNotExist:
            shop_cart = shop_cart_model(
                user=self.user,
                product=product,
                qty=qty,
                product_color=color,
            )
            total_price = product.get_price_by_discount() * qty
            if color != None:
                total_price += color.value_added * qty
            shop_cart.total_price = total_price
        finally:
            shop_cart.save()
            self.count_shop_cart()

    def delete_from_shop_cart(self, shopcart_id):
        shop_cart = shop_cart_model.objects.filter(
            Q(user=self.user) & Q(id=shopcart_id) & Q(order=None)
        )
        shop_cart.delete()
        self.count_shop_cart()

    def update_shop_cart(self, shopcart_id, qty):
        shop_cart = shop_cart_model.objects.get(
            Q(user=self.user) & Q(id=shopcart_id) & Q(order=None)
        )
        shop_cart.qty += qty
        if shop_cart.qty > shop_cart.product.get_number_in_warehouse():
            shop_cart.qty = shop_cart.product.get_number_in_warehouse()
        if shop_cart.qty <= 0:
            shop_cart.delete()
        else:
            # if not (
            #     shop_cart.product.get_number_in_my_order() + qty
            #     > shop_cart.product.get_number_in_warehouse()
            # ):
            total_price = shop_cart.qty * shop_cart.product.get_price_by_discount()
            if shop_cart.product_color != None:
                total_price += shop_cart.product_color.value_added * shop_cart.qty
            shop_cart.total_price = total_price
            shop_cart.save()
        self.count_shop_cart()
