from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from auth_app.forms import SignupForm, LoginForm
from base.utils.custom_user_passes_test import CustomLoginRequiredMixin


class LoginView(CustomLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm()
        context = {"form": form}
        return render(request, "auth_app/auth_login.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            user = authenticate(username=phone, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Login Successful")
            else:
                return HttpResponse("Login Failed")
        return render(request, "auth_app/auth_login.html", {"form": form})
