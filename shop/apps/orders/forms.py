from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator

from .models import PaymentType


class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=3,
        label="نام",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام",
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
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی",
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
        label="ایمیل",
        validators=[EmailValidator(message="ایمیل وارد شده صحیح نمی باشد")],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ایمیل",
            }
        ),
        required=False,
    )
    address = forms.CharField(
        label="آدرس",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
            }
        ),
        error_messages={"required": "فیلد آدرس می بایستی پر شود"},
    )
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل",
            }
        ),
        error_messages={"required": "فیلد شماره موبایل می بایستی پر شود"},
    )
    description = forms.CharField(
        label="توضیحات",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
            }
        ),
        required=False,
    )
    payment_type = forms.ChoiceField(
        label="روش پرداخت",
        widget=forms.RadioSelect(),
        choices=[(item.id, item) for item in PaymentType.objects.all()],
    )

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
