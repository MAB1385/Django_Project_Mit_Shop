from django.urls import path

from .views import (ChangePasswordUserPanelView, ChangePasswordView,
                    LastOrders, LoginUserView, LogoutUserView,
                    RegisterUserView, RememberPasswordView,
                    ReSendRegisterCodeView, ShowUserPaymentsView,
                    UpdateProfileView, UserPanelView, VerifyRegisterCodeView,
                    WelcomeView)

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("verify/", VerifyRegisterCodeView.as_view(), name="verify"),
    path("verify/re_send/", ReSendRegisterCodeView.as_view(), name="resend_code"),
    path("welcome/", WelcomeView.as_view(), name="welcome"),
    path("login/", LoginUserView.as_view(), name="login"),
    path(
        "login/change_password/", ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "user/change_password/",
        ChangePasswordUserPanelView.as_view(),
        name="change_password_user_panel",
    ),
    path(
        "login/remember_password/",
        RememberPasswordView.as_view(),
        name="remember_password",
    ),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("user/panel/", UserPanelView.as_view(), name="user_panel"),
    path("user/show_last_orders/", LastOrders.as_view(), name="show_last_orders"),
    path("user/update_profile/", UpdateProfileView.as_view(), name="update_profile"),
    path("user/show_user_payments/", ShowUserPaymentsView.as_view(), name="show_user_payments"),
]
