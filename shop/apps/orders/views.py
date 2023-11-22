from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from utils import price_by_delivery_tax

from apps.accounts.models import Customer
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from apps.products.models import Product, ProductColor

from .forms import OrderForm
from .models import Order, PaymentType
from .models import ShopCart as shop_cart_model
from .shop_cart import ShopCart

#! To base address root
BASE_ORDERS = "orders/"
BASE_PARTIALS = "orders/partials/"

#! To display shop cart
class ShopCartView(LoginRequiredMixin, View):
    template_name = BASE_ORDERS + "shop_cart.html"

    def get(self, *args, **kwargs):
        shop_cart = ShopCart(self.request)
        return render(self.request, self.template_name, {"shop_cart": shop_cart})


# todo --------------------------------------------------------------------
#! To add shop cart ---> ajax
def add_to_shop_cart(request):

    if not request.user.is_authenticated:
        response = JsonResponse(
            {
                "success": False,
                "error": "user",
            }
        )
        response.status_code = 403
        print(response)
        return response
    shop_cart = ShopCart(request)
    product_id = request.GET.get("product_id")
    qty = request.GET.get("qty")
    color_id = request.GET.get("color_id")
    product = get_object_or_404(Product, id=product_id)
    if color_id == "0":
        colors = list(product.product_colors.all())
        if len(colors) == 0:
            color = None
        else:
            color = colors[0]
    elif color_id == "None":
        response = JsonResponse(
            {
                "success": False,
                "error": "color",
                "count": shop_cart.count,
            }
        )
        response.status_code = 403
        return response
    else:
        color = get_object_or_404(ProductColor, id=color_id)
    shop_cart.add_to_shop_cart(product, int(qty), color)
    response = JsonResponse({"success": True, "count": shop_cart.count})
    response.status_code = 200
    return response


# todo --------------------------------------------------------------------
#! To delete from shop cart ---> ajax
@login_required
def delete_from_shop_cart(request):
    shopcart_id = request.GET.get("shopcart_id")
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(shopcart_id)
    return redirect("orders:show_shop_cart")


# todo --------------------------------------------------------------------
#! To show update shop cart ---> ajax , render_partial
@login_required
def show_shop_cart(request):
    shop_cart_ = ShopCart(request)
    shop_cart = shop_cart_model.objects.filter(Q(user=request.user) & Q(order=None))
    for i in shop_cart:
        shop_cart_.update_shop_cart(i.id, 0)
    shop_cart = shop_cart_model.objects.filter(Q(user=request.user) & Q(order=None))
    total_price = 0
    for item in shop_cart:
        total_price += item.total_price
    order_finaly_price, delivery, tax = price_by_delivery_tax(total_price)
    context = {
        "shop_cart": shop_cart,
        "total_price": total_price,
        "delivery": delivery,
        "tax": int(tax),
        "order_finaly_price": order_finaly_price,
    }
    return render(
        request,
        BASE_PARTIALS + "show_shop_cart.html",
        context,
    )


# todo --------------------------------------------------------------------
#! To subtract the number from shop cart ---> ajax
@login_required
def update_shop_cart(request):
    shopcart_id = request.GET.get("shopcart_id")
    qty = request.GET.get("qty")
    shop_cart = ShopCart(request)
    shop_cart.update_shop_cart(shopcart_id, int(qty))
    return redirect("orders:show_shop_cart")


# todo --------------------------------------------------------------------
#! To number of products in shop cart ---> ajax
def status_of_shop_cart(request):
    if request.user.is_authenticated:
        shop_cart = ShopCart(request)
        return HttpResponse(shop_cart.count)
    else:
        return HttpResponse(0)


# todo --------------------------------------------------------------------
#! dict products from shop cart ---> product_id:qty
def shop_cart_dict(request):
    if request.user.is_authenticated:
        shop_cart = ShopCart(request)
        context = {"shop_cart_dict": shop_cart.shop_cart_dict}
    else:
        context = {"shop_cart_dict": dict({})}
    return context


# todo --------------------------------------------------------------------
#! To create order ---> Continue shopping
class CreateOrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create(
                user=self.request.user,
            )
        order = Order.objects.create(
            customer=customer, payment_type=get_object_or_404(PaymentType, id=1)
        )
        shop_cart = shop_cart_model.objects.filter(
            Q(user=self.request.user) & Q(order=None)
        )
        shop_cart.update(order=order)
        return redirect("orders:checkout_order", order.id)


# todo --------------------------------------------------------------------
#! To check out order
class CheckOutOrderView(LoginRequiredMixin, View):
    template_name = "checkout_order.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        customer = get_object_or_404(Customer, user=user)
        order = get_object_or_404(Order, id=kwargs["order_id"])
        if order.is_finaly or order.customer != customer:
            messages.error(self.request, "فاکتور وارد شده اشتباه می باشد.", "danger")
            return redirect("main:home")
        shop_cart = shop_cart_model.objects.filter(Q(user=user) & Q(order=order))
        total_price = 0
        for item in shop_cart:
            total_price += item.total_price
        order_finaly_price, delivery, tax = price_by_delivery_tax(
            total_price, order.discount
        )

        data = {
            "name": user.name,
            "family": user.family,
            "email": user.email,
            "phone_number": customer.phone_number,
            "address": customer.address,
            "description": order.description,
            "payment_type": order.payment_type,
        }

        form = OrderForm(data)

        form_coupon = CouponForm()

        context = {
            "shop_cart": shop_cart,
            "total_price": total_price,
            "delivery": delivery,
            "tax": int(tax),
            "order": order,
            "order_finaly_price": int(order_finaly_price),
            "form": form,
            "form_coupon": form_coupon,
        }

        return render(
            self.request,
            BASE_ORDERS + self.template_name,
            context,
        )

    def post(self, *args, **kwargs):
        form = OrderForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                order = Order.objects.get(id=kwargs["order_id"])
                order.description = data["description"]
                order.payment_type = PaymentType.objects.get(
                    id=int(data["payment_type"])
                )
                order.save()
                print(data["payment_type"])
                user = self.request.user
                user.name = data["name"]
                user.family = data["family"]
                user.email = data["email"]
                user.save()

                customer = Customer.objects.get(user=user)
                customer.phone_number = data["phone_number"]
                customer.address = data["address"]
                customer.save()

                match int(data["payment_type"]):
                    case 1:  #!Online payment
                        return redirect("payments:zarinpal_payment", kwargs["order_id"])
                    case 2:  #!Payment by bank slip
                        pass
                    case 3:  #!Payment on the spot
                        pass
                    case _:
                        messages.error(
                            self.request, "اطلاعات وارد شده نادرست می باشد.", "danger"
                        )
            except ObjectDoesNotExist:
                messages.error(self.request, "فاکتوری یافت نشد.", "danger")
            finally:
                return redirect("orders:checkout_order", kwargs["order_id"])
        else:
            messages.error(self.request, "اطلاعات وارد شده نادرست می باشد.", "danger")
            return redirect("orders:checkout_order", kwargs["order_id"])


# todo --------------------------------------------------------------------
#! To applay coupon
class ApplayCoupon(View):
    def post(self, *args, **kwargs):
        order_id = kwargs["order_id"]
        form = CouponForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            coupon_code = data["coupon_code"]
            coupon = Coupon.objects.filter(
                Q(coupon_code=coupon_code)
                & Q(is_active=True)
                & Q(start_date__lte=datetime.now())
                & Q(end_date__gte=datetime.now())
            )
            discount = 0
            try:
                order = Order.objects.get(id=order_id)
                if coupon:
                    discount = coupon[0].discount
                    order.discount = discount
                    order.save()
                    messages.success(self.request, "تخفیف با موفقیت اعمال شد.")
                    return redirect("orders:checkout_order", order_id)
                else:
                    order.discount = discount
                    order.save()
                    messages.error(self.request, "کد وارد شده معتبر نیست.", "danger")
                    return redirect("orders:checkout_order", order_id)
            except ObjectDoesNotExist:
                messages.error(self.request, "سفارش موجود نیست.", "danger")
            finally:
                return redirect("orders:checkout_order", order_id)
