from django import forms
from auth_app.models import User


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone", "password", "confirm_password")

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password


class LoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
