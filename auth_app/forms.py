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


class CivilRegistry(forms.Form):
    birth_day = forms.DateField(
        widget=forms.DateInput(
            format='%Y/%m/%d',
            attrs={
                "class": "form-control",
                "placeholder": "1379/07/30",
                "type": "text"
            }
        ),
        input_formats=['%Y/%m/%d']
    )
    national_id = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "1234567890",
                "type": "number"
            }
        )
    )
