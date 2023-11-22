from django import forms


class CouponForm(forms.Form):
    coupon_code = forms.CharField(
        label="کد تخفیف",
        error_messages={"required": "این فیلد می بایستی پر شود"},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "کد تخفیف"}
        ),
    )
