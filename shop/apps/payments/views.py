import json

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.models import Customer
from apps.orders.models import Order, OrderState
from apps.warehouses.models import Warehouse, WarehouseType

from .models import Payment

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "این تراکنش توسط درگاه پرداخت زرین پال انجام می شود."
CallbackURL = "http://127.0.0.1:8000/payments/verify/"


# todo --------------------------------------------------------------------
class ZarinpalPaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs["order_id"])
            user = self.request.user
            payment = Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=self.request.user),
                amount=order.get_order_total_price(),
                description=description,
            )
            payment.save()
            self.request.session["payment_session"] = {
                "order_id": order.id,
                "payment_id": payment.id,
            }
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.get_order_total_price(),
                "Description": description,
                "Phone": user.mobail_number,
                "CallbackURL": CallbackURL,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {
                "content-type": "application/json",
                "content-length": str(len(data)),
            }
            try:
                response = requests.post(
                    ZP_API_REQUEST, data=data, headers=headers, timeout=10
                )

                if response.status_code == 200:
                    response = response.json()
                    if response["Status"] == 100:
                        return {
                            "status": True,
                            "url": ZP_API_STARTPAY + str(response["Authority"]),
                            "authority": response["Authority"],
                        }
                    else:
                        return {"status": False, "code": str(response["Status"])}
                return response

            except requests.exceptions.Timeout:
                return {"status": False, "code": "timeout"}
            except requests.exceptions.ConnectionError:
                return {"status": False, "code": "connection error"}
        except ObjectDoesNotExist:
            return redirect("orders:checkout_order", kwargs["order_id"])


# todo --------------------------------------------------------------------
class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order_id = self.request.session["payment_session"]["order_id"]
        payment_id = self.request.session["payment_session"]["payment_id"]
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(id=payment_id)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_order_total_price(),
            "Authority": kwargs["authority"],
        }
        data = json.dumps(data)
        # set content length by data
        headers = {"content-type": "application/json", "content-length": str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                order.is_finaly = True
                order.order_state = OrderState.objects.get(id=1)
                order.save()
                payment.is_finally = True
                payment.ref_id = str(response["RefID"])
                payment.status_code = response["Status"]
                payment.save()
                for item in order.orders_details.all():
                    Warehouse.objects.create(
                        warehouse_type=WarehouseType.objects.get(id=2),
                        user_registered=self.request.user,
                        product=item.product,
                        qty=item.qty,
                        price=item.price,
                    )
                return redirect(
                    "payments:show_verify_message",
                    f'پرداخت با موفقیت انجام شد. کد پیگیری : {response["RefID"]}',
                )
            else:
                payment.status_code = response["Status"]
                payment.save()
                return redirect(
                    "payments:show_verify_message",
                    f'پرداخت با موفقیت انجام نشد. کد خطا : {response["Status"]}',
                )
        return response


# todo --------------------------------------------------------------------
def show_verify_message(request, message):
    return render(request, "payments/verify_message.html", {"message": message})
