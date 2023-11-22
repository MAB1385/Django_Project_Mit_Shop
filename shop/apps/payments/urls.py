from django.urls import path

from .views import ZarinpalPaymentVerifyView, ZarinpalPaymentView, show_verify_message

app_name = "payments"
urlpatterns = [
    path(
        "zarinpal_payment/<int:order_id>/",
        ZarinpalPaymentView.as_view(),
        name="zarinpal_payment",
    ),
    path(
        "verify/<str:authority>/",
        ZarinpalPaymentVerifyView.as_view(),
        name="zarinpal_payment_verify",
    ),
    path(
        "show_verify_message/<str:message>/",
        show_verify_message,
        name="show_verify_message",
    ),
]
