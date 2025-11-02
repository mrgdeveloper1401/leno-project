from django import forms

class RequestPhoneForm(forms.Form):
    phone = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری را وارد کنید',
            'id': 'username'
        })
    )


class VerifyRequestPhoneForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label="کد تایید",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد تایید را وارد کنید',
            'id': 'code'
        })
    )
