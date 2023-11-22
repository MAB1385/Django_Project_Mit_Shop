from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator

from .models import CustomUser


#! form to create user:
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="RePassword")
    email = forms.EmailField(
        label="Email",
        validators=[EmailValidator(message="ایمیل وارد شده صحیح نمی باشد")],
    )
    name = forms.CharField(
        label="Name",
        validators=[
            RegexValidator(
                r"^[A-Za-z\u0600-\u06FF\s]+$", message="نام وارد شده صحیح نمی باشد"
            )
        ],
    )
    family = forms.CharField(
        label="Family",
        validators=[
            RegexValidator(
                r"^[A-Za-z\u0600-\u06FF\s]+$", message="فامیلی وارد شده صحیح نمی باشد"
            )
        ],
    )
    mobail_number = forms.CharField(
        label="Mobai_Number",
        error_messages={"unique": "این شماره تلفن قبلا استفاده شده"},
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
        error_messages={"required": "ربات نبودن می بایستی تایید شود"},
        help_text="<br><br>",
    )

    class Meta:
        model = CustomUser
        fields = ["mobail_number", "email", "name", "family", "gender"]

    def clean_mobail_number(self):
        mobail_number = self.cleaned_data["mobail_number"]
        if not mobail_number:  # ? Chake mobail_number
            raise ValidationError("باید شماره موبایل را وارد کنید")
        if (
            len(mobail_number) != 11
            or "09" != mobail_number[:2]
            or mobail_number.isdigit() == False
        ):  # ? Chake mobail_number
            raise ValidationError("این شماره موبایل نا معتبر می باشد")
        return mobail_number

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن باهم مغایرت دارند")
        return pass2

    #! Rewriting the save function:
    def save(self, commit=True):  # ? commit --> End work --> Permission to save
        user = super().save(commit=False)  # ? Do not save
        user.set_password(self.cleaned_data["password1"])
        if commit:  # ? Save if allowed
            user.save()
        return user


# todo ------------------------------------------------------------------------------
#! form to chage user:
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید."
    )  # ? Makes the password read-only

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
        error_messages={"required": "ربات نبودن می بایستی تایید شود"},
    )

    class Meta:
        model = CustomUser
        fields = [
            "mobail_number",
            "password",
            "email",
            "name",
            "family",
            "gender",
            "is_active",
            "is_admin",
        ]


# todo ------------------------------------------------------------------------------
#! form to register user:
class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور را وارد کنید"}
        ),
        label="رمز عبور",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور را وارد کنید",
            }
        ),
        label="تکرار رمز عبور",
    )
    mobail_number = forms.CharField(
        label="شماره موبایل",
        error_messages={"unique": "این نام کابری قبلا استفاده شده"},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل را وارد کنید",
                "maxlength": "11",
            }
        ),
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
        error_messages={"required": "ربات نبودن می بایستی تایید شود"},
    )

    class Meta:
        model = CustomUser
        fields = ["mobail_number", "password"]

    def clean_mobail_number(self):
        mobail_number = self.cleaned_data["mobail_number"]
        if not mobail_number:  # ? Chake mobail_number
            raise ValidationError("باید شماره موبایل را وارد کنید")
        if (
            len(mobail_number) != 11
            or "09" != mobail_number[:2]
            or mobail_number.isdigit() == False
        ):  # ? Chake mobail_number
            raise ValidationError("این شماره موبایل نامعتبر می باشد")
        return mobail_number

    def clean_password2(self):  # ? Chacke password
        pass1 = self.cleaned_data["password"]
        pass2 = self.cleaned_data["password2"]
        if len(pass1) < 6:
            # // self.password.widget = forms.PasswordInput(
            # //    attrs={
            # //         "class": "form-control alert-danger",
            # //        "placeholder": "رمز عبور را وارد کنید",
            # //    }
            # // )
            raise ValidationError("رمز عبور باید بیشتر از 6 کاراکتر باشد")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن باهم مغایرت دارند")
        return pass2


# todo ------------------------------------------------------------------------------
#! for verify register code
class VerifyRegisterCodeForm(forms.Form):
    active_code = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کد دریافتی را وارد کنید"}
        ),
        error_messages={"required": "این فیلد نمی تواند خالی باشد"},
    )

    def clean_active_code(self):
        active_code = self.cleaned_data["active_code"]
        if active_code.isdigit() == False:
            raise ValidationError("کد وارد شده نادرست می باشد")
        return active_code


# todo ------------------------------------------------------------------------------
class LoginUserForm(forms.Form):
    mobail_number = forms.CharField(
        label="شماره موبایل",
        error_messages={"unique": "این نام کابری قبلا استفاده شده"},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل را وارد کنید",
                "maxlength": "11",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور را وارد کنید"}
        ),
        label="رمز عبور",
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
        error_messages={"required": "ربات نبودن می بایستی تایید شود"},
    )

    def clean_mobail_number(self):
        mobail_number = self.cleaned_data["mobail_number"]
        if not mobail_number:  # ? Chake mobail_number
            raise ValidationError("باید شماره موبایل را وارد کنید")
        if (
            len(mobail_number) != 11
            or "09" != mobail_number[:2]
            or mobail_number.isdigit() == False
        ):  # ? Chake mobail_number
            raise ValidationError("این شماره موبایل نامعتبر می باشد")
        return mobail_number


# todo ------------------------------------------------------------------------------
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور را وارد کنید"}
        ),
        label="رمز عبور",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور را وارد کنید",
            }
        ),
        label="تکرار رمز عبور",
    )

    def clean_password2(self):  # ? Chacke password
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if len(pass1) < 6:
            raise ValidationError("رمز عبور باید بیشتر از 6 کاراکتر باشد")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن باهم مغایرت دارند")
        return pass2


# todo ------------------------------------------------------------------------------
class RememberPasswordForm(forms.Form):
    mobail_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل را وارد کنید",
                "maxlength": "11",
            }
        ),
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
        error_messages={"required": "ربات نبودن می بایستی تایید شود"},
    )

    def clean_mobail_number(self):
        mobail_number = self.cleaned_data["mobail_number"]
        if not mobail_number:  # ? Chake mobail_number
            raise ValidationError("باید شماره موبایل را وارد کنید")
        if (
            len(mobail_number) != 11
            or "09" != mobail_number[:2]
            or mobail_number.isdigit() == False
        ):  # ? Chake mobail_number
            raise ValidationError("این شماره موبایل نامعتبر می باشد")
        return mobail_number


# todo ------------------------------------------------------------------------------
class UpdateProfileForm(forms.Form):
    mobail_number = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل را وارد کنید",
                "maxlength": "11",
                "readonly": "readonly",
            }
        ),
    )
    name = forms.CharField(
        max_length=100,
        min_length=3,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خود را وارد کنید",
            }
        ),
        error_messages={"required": "فیلد نام می بایستی پر شود"},
        validators=[
            RegexValidator(
                r"^[A-Za-z\u0600-\u06FF\s]+$", message="نام وارد شده صحیح نمی باشد"
            )
        ],
    )
    family = forms.CharField(
        max_length=100,
        min_length=3,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید",
            }
        ),
        error_messages={"required": "فیلد نام خانوادگی می بایستی پر شود"},
        validators=[
            RegexValidator(
                r"^[A-Za-z\u0600-\u06FF\s]+$",
                message="نام خانوادگی وارد شده صحیح نمی باشد",
            )
        ],
    )
    email = forms.EmailField(
        max_length=300,
        label="",
        validators=[EmailValidator(message="ایمیل وارد شده صحیح نمی باشد")],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ایمیل خود را وارد کنید",
            }
        ),
        error_messages={"required": "فیلد ایمیل می بایستی پر شود"},
    )
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل خود را وارد کنید",
            }
        ),
        error_messages={"required": "فیلد شماره موبایل می بایستی پر شود"},
    )
    address = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "آدرس خود را وارد کنید",
            }
        ),
        error_messages={"required": "فیلد آدرس می بایستی پر شود"},
    )
    image = forms.ImageField(label="", required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number:  # ? Chake phone_number
            raise ValidationError("باید شماره موبایل را وارد کنید")
        if (
            len(phone_number) != 11
            or "09" != phone_number[:2]
            or phone_number.isdigit() == False
        ):  # ? Chake phone_number
            raise ValidationError("شماره موبایل نامعتبر می باشد")
        return phone_number
