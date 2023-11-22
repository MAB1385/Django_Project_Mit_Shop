from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View
from utils import create_random_code, send_sms

from apps.orders.models import Order
from apps.payments.models import Payment

from .forms import (
    ChangePasswordForm,
    LoginUserForm,
    RegisterUserForm,
    RememberPasswordForm,
    UpdateProfileForm,
    VerifyRegisterCodeForm,
)
from .models import Customer, CustomUser

#! To base address root
BASE_ACCOUNTS = "accounts/"
BASE_PARTIALS = "accounts/partials/"

#! Create your views here.
class RegisterUserView(View):
    def dispatch(
        self, *args, **kwargs
    ):  # ? It is executed before other functions are executed
        if self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(
            self.request, *args, **kwargs
        )  # ? Finally, the parent must be called

    template_name = BASE_ACCOUNTS + "register.html"

    def get(self, *args, **kwargs):
        form = RegisterUserForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = RegisterUserForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = create_random_code(5)
            CustomUser.objects.create_user(
                mobail_number=data["mobail_number"],
                active_code=active_code,
                password=data["password"],
            )
            send_sms(
                data["mobail_number"],
                f"با سلام \n کد فعال سازی پنل کاربری شما در فروشگاه میت شاپ {active_code} می باشد.",
            )
            self.request.session["user_session"] = {
                "active_code": str(active_code),
                "mobail_number": data["mobail_number"],
                "remember_password": False,
            }
            messages.success(
                self.request,
                "اطلاعات شما با موفقیت ثبت شد.\nجهت فعال سازی کد را وارد کنید.",
                "success",
            )
            return redirect("accounts:verify")
        messages.error(self.request, "اشتباهی در فرایند ثبت نام رخ داده است.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
class VerifyRegisterCodeView(View):
    def dispatch(
        self, *args, **kwargs
    ):  # ? It is executed before other functions are executed
        if self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(
            self.request, *args, **kwargs
        )  # ? Finally, the parent must be called

    template_name = BASE_ACCOUNTS + "verify_register_code.html"

    def get(self, *args, **kwargs):
        form = VerifyRegisterCodeForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = VerifyRegisterCodeForm(self.request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user_session = self.request.session["user_session"]
            user = CustomUser.objects.get(mobail_number=user_session["mobail_number"])
            if data["active_code"] == user_session["active_code"]:
                user = CustomUser.objects.get(
                    mobail_number=user_session["mobail_number"]
                )
                if user_session["remember_password"] == False:
                    user.is_active = True
                    active_code = create_random_code(5)
                    user.active_code = active_code
                    user.save()
                    login(self.request, user)
                    messages.success(
                        self.request, "ثبت نام با موفقیت انجام شد.", "success"
                    )
                    return redirect("accounts:welcome")
                else:
                    return redirect("accounts:change_password")
            else:
                messages.error(self.request, "کد وارد شده اشتباه می باشد.", "danger")
                return render(self.request, self.template_name, {"form": form})
        messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
class WelcomeView(View):
    template_name = BASE_ACCOUNTS + "welcome.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


# todo ---------------------------------------------------------------------------------------
class LoginUserView(View):
    def dispatch(
        self, *args, **kwargs
    ):  # ? It is executed before other functions are executed
        if self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(
            self.request, *args, **kwargs
        )  # ? Finally, the parent must be called

    template_name = BASE_ACCOUNTS + "login.html"

    def get(self, *args, **kwargs):
        form = LoginUserForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = LoginUserForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data["mobail_number"], password=data["password"]
            )
            if user is not None:
                messages.success(self.request, "ورود با موفقیت انجام شد.", "success")
                login(self.request, user)
                next_url = self.request.GET.get("next")
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect("main:home")
            else:
                messages.error(self.request, "کاربری یافت نشد.", "danger")
                return render(self.request, self.template_name, {"form": form})
        messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
class LogoutUserView(View):
    def dispatch(
        self, *args, **kwargs
    ):  # ? It is executed before other functions are executed
        if not self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(
            self.request, *args, **kwargs
        )  # ? Finally, the parent must be called

    def get(self, *args, **kwargs):
        #! To save sessions beford of logout ---> To prevent sessions from being deleted after logout
        # ? session_data=self.request.session.get('shop_cart')
        logout(self.request)
        # ? self.request.session.['shop_cart'] = session_data
        return redirect("main:home")


# todo ---------------------------------------------------------------------------------------
class UserPanelView(
    LoginRequiredMixin, View
):  # ? LoginRequiredMixin --> You must be logged in to call this class
    template_name = BASE_ACCOUNTS + "user_panel.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            customer = Customer.objects.get(user=user)
            user_info = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobail_number": user.mobail_number,
                "phone_number": customer.phone_number,
                "address": customer.address,
                "image": customer.image,
            }
        except ObjectDoesNotExist:
            user_info = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobail_number": user.mobail_number,
            }
        return render(self.request, self.template_name, {"user_info": user_info})


# todo ---------------------------------------------------------------------------------------
class ReSendRegisterCodeView(View):
    def get(self, *args, **kwargs):
        active_code = create_random_code(5)
        user_session = self.request.session["user_session"]
        user = CustomUser.objects.get(mobail_number=user_session["mobail_number"])
        user.active_code = active_code
        user.save()
        if user_session["remember_password"] == False:
            send_sms(
                user_session["mobail_number"],
                f"با سلام \n کد فعال سازی پنل کاربری شما در فروشگاه میت شاپ {active_code} می باشد.",
            )
            self.request.session["user_session"] = {
                "active_code": str(active_code),
                "mobail_number": user_session["mobail_number"],
                "remember_password": False,
            }
        else:
            send_sms(
                user_session["mobail_number"],
                f"با سلام \n کد تایید شماره موبایل شما در فروشگاه میت شاپ {active_code} می باشد.",
            )
            self.request.session["user_session"] = {
                "active_code": str(active_code),
                "mobail_number": user_session["mobail_number"],
                "remember_password": True,
            }
        return redirect("accounts:verify")


# todo ---------------------------------------------------------------------------------------
#! for change password
class ChangePasswordView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(self.request, *args, **kwargs)

    template_name = BASE_ACCOUNTS + "change_password.html"

    def get(self, *args, **kwargs):
        form = ChangePasswordForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = ChangePasswordForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = self.request.session["user_session"]
            user = CustomUser.objects.get(mobail_number=user_session["mobail_number"])
            user.set_password(data["password1"])
            user.active_code = create_random_code(5)
            user.save()
            messages.success(
                self.request, "رمز عبور شما با موفقیت تغییر کرد.", "success"
            )
            return redirect("accounts:login")
        messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
#! for get mobail number to change password
class RememberPasswordView(View):
    def dispatch(
        self, *args, **kwargs
    ):  # ? It is executed before other functions are executed
        if self.request.user.is_authenticated:
            return redirect("main:home")
        return super().dispatch(
            self.request, *args, **kwargs
        )  # ? Finally, the parent must be called

    template_name = BASE_ACCOUNTS + "remember_password.html"

    def get(self, *args, **kwargs):
        form = RememberPasswordForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = RememberPasswordForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(mobail_number=data["mobail_number"])
                active_code = create_random_code(5)
                user.active_code = active_code
                user.save()
                send_sms(
                    data["mobail_number"],
                    f"با سلام \n کد تایید سازی شماره موبایل شما در فروشگاه میت شاپ {active_code} می باشد.",
                )
                self.request.session["user_session"] = {
                    "active_code": str(active_code),
                    "mobail_number": data["mobail_number"],
                    "remember_password": True,
                }
                messages.success(
                    self.request,
                    "جهت تغییر رمز عبور خود کد دریافتی را ارسال نمایید.",
                    "success",
                )
                return redirect("accounts:verify")
            except CustomUser.DoesNotExist:
                messages.error(
                    self.request, "کاربری با این شماره موبایل موجود نمی باشد.", "danger"
                )
                return render(self.request, self.template_name, {"form": form})
        messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
#! for display last orders
class LastOrders(LoginRequiredMixin, View):
    template_name = BASE_PARTIALS + "show_last_orders.html"

    def get(self, *args, **kwargs):
        orders = Order.objects.filter(customer_id=self.request.user.id).order_by(
            "-register_date"
        )[:4]
        return render(self.request, self.template_name, {"orders": orders})


# todo ---------------------------------------------------------------------------------------
#! for update profile
class UpdateProfileView(LoginRequiredMixin, View):
    template_name = BASE_ACCOUNTS + "update_profile.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        image_url = None
        try:
            customer = Customer.objects.get(user=user)
            initial_dict = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobail_number": user.mobail_number,
                "phone_number": customer.phone_number,
                "address": customer.address,
            }
            image_url = customer.image
        except ObjectDoesNotExist:
            initial_dict = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobail_number": user.mobail_number,
            }
        form = UpdateProfileForm(initial=initial_dict)
        return render(
            self.request, self.template_name, {"form": form, "image_url": image_url}
        )

    def post(self, *args, **kwargs):
        form = UpdateProfileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = self.request.user
            user.name = cd["name"]
            user.family = cd["family"]
            user.email = cd["email"]
            user.save()
            try:
                customer = Customer.objects.get(user=user)
                customer.phone_number = cd["phone_number"]
                customer.address = cd["address"]
                if cd["image"]:
                    customer.image = cd["image"]
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=self.request.user,
                    phone_number=cd["phone_number"],
                    address=cd["address"],
                    image=cd["image"],
                )
            messages.success(self.request, "تغییرات با موفقیت اعمال شد", "success")
            return redirect("accounts:user_panel")
        else:
            messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد", "danger")
            return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
#! for change password
class ChangePasswordUserPanelView(LoginRequiredMixin, View):

    template_name = BASE_ACCOUNTS + "change_password_user_panel.html"

    def get(self, *args, **kwargs):
        form = ChangePasswordForm()
        return render(self.request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = ChangePasswordForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = self.request.user
            user.set_password(data["password1"])
            user.active_code = create_random_code(5)
            user.save()
            messages.success(
                self.request, "رمز عبور شما با موفقیت تغییر کرد.", "success"
            )
            return redirect("accounts:login")
        messages.error(self.request, "اطلاعات وارد شده معتبر نمی باشد.", "danger")
        return render(self.request, self.template_name, {"form": form})


# todo ---------------------------------------------------------------------------------------
class ShowUserPaymentsView(LoginRequiredMixin, View):
    template_name = BASE_ACCOUNTS + "show_user_payments.html"

    def get(self, *args, **kwargs):
        payments = Payment.objects.filter(customer_id=self.request.user.id).order_by(
            "-register_date"
        )[:20]
        return render(self.request, self.template_name, {"payments": payments})
