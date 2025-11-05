from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from auth_app.clasess import AuthService
from auth_app.clasess.profile import ProfileService
from auth_app.models import UserToken
from auth_app.forms import (
    RequestPhoneForm,
    VerifyRequestPhoneForm,
    CivilRegistry
)
from base.utils.mixin import RedirectAuthenticatedUserMixin
from auth_app.tasks import task_logout_user


class RequestPhoneView(RedirectAuthenticatedUserMixin, View):
    template_name = "auth_app/login/auth-signup-login.html"
    form_class = RequestPhoneForm

    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            login_service = AuthService()
            result = login_service.send_login_request(phone)

            if result['Success']:
                request.session['phone'] = phone

                display_message =  "کد تأیید به شماره شما ارسال شد"
                messages.success(request, display_message)
                return redirect("auth_app:verify")
            else:
                messages.error(request, result['Error'])

        return render(request, self.template_name, {"form": form})


class VerifyRequestPhoneView(RedirectAuthenticatedUserMixin, View):
    template_name = "auth_app/login/auth-signup-login-verify.html"
    form_class = VerifyRequestPhoneForm

    def get(self, request: HttpRequest):
        phone = request.session.get('phone')
        if phone is None:
            return redirect('auth_app:login')
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = request.session['phone']
            code = form.cleaned_data['code']

            verify_service = AuthService()
            result = verify_service.verify_code(phone, code) # verify otp code
            if result['Success']:
                # create user
                random_password = get_random_string(16)
                hashed_password = make_password(random_password)
                user = User.objects.filter(username=phone).only("id") # check user
                if not user.exists():
                    User.objects.create_user(username=phone, password=hashed_password, email=None)

                # save token in database
                get_user = user.first()
                res = result['Result']
                UserToken.objects.create(
                    user_id=get_user.id,
                    access_token=res.get('access_token'),
                    refresh_token=res.get('refresh_token'),
                    expire_in_timestamp=res['user']['expire_in_timestamp']
                )

                # login user
                auth_login(request, get_user)

                # remove session
                self._clean_verification_session(request)

                messages.success(request, "احراز هویت با موفقیت انجام شد")
                return redirect('auth_app:login') # TODO, redirect user profile

            else:
                messages.error(request, result['Error'])

        return render(request, self.template_name, {"form": form})


    def _clean_verification_session(self, request):
        """remove session"""
        keys_to_remove = ['phone']
        for key in keys_to_remove:
            if key in request.session:
                del request.session[key]


class ProfileView(LoginRequiredMixin, View):
    template_name = "auth_app/profile/auth-profile.html"

    def get(self, request: HttpRequest):
        profile = ProfileService()

        # get token
        user_access_token = UserToken.objects.filter(
            user_id=request.user.id
        ).only("access_token").last()

        if user_access_token:
            # send token into service
            response = profile.get_profile_details(user_access_token.access_token)
            response_success = response['Success']

            context_data = {}

            if response_success.lower() == "true":
                context_data["data"] = response['Result']
                context_data["is_error"] = False
                return render(request, self.template_name, context_data)
            else:
                error_response = response['Error']
                context_data["data"] = error_response
                context_data["is_error"] = True
                return render(request, self.template_name, context_data)
        return render(request, self.template_name)


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        # get token by user
        user_token = UserToken.objects.filter(
            user_id=request.user.id
        ).only(
            "refresh_token",
            "access_token"
        ).last()

        if user_token:
            auth = AuthService()
            access_token=user_token.access_token
            refresh_token=user_token.refresh_token
            task_logout_user.delay(access_token, refresh_token)

        auth_logout(request)
        messages.success(request, "شما با موفقیت از حساب خود خارج شدید")
        return redirect("auth_app:logout_template")
    else:
        return redirect("auth_app:login")


class LogOutTemplateView(TemplateView):
    template_name = "auth_app/logout/auth-logout.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth = AuthService()

            # get token
            user_token = UserToken.objects.filter(user_id=request.user.id).only(
                "access_token",
                "refresh_token"
            ).last()

            if user_token:
                # send request into api for logout user
                auth.logout(user_token.access_token, user_token.refresh_token)

            # logout in django
            auth_logout(request)
        return super().dispatch(request, *args, **kwargs)


class CivilRegistryView(LoginRequiredMixin, View):
    template_name = "auth_app/civil_registry/civil_registry.html"
    form = CivilRegistry

    def get(self, request: HttpRequest):
        form = self.form()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form(request.POST)
        context_data = {"form": form}

        if form.is_valid():
            birth_day = form.cleaned_data['birth_day']
            national_id = form.cleaned_data['national_id']

            try:
                # get token
                access_token = UserToken.objects.filter(
                    user_id=request.user.id
                ).only(
                    "access_token",
                ).last().access_token

                if access_token:
                    # send request into api
                    auth = AuthService()
                    birth_day = str(birth_day).split("-")
                    birth_day = '/'.join(birth_day)
                    result = auth.civil_registry(birth_day, national_id, access_token)

                    # return data into template
                    if result['Success']:
                        context_data["data"] = result['Result']
                        context_data["is_error"] = False
                        return render(request, self.template_name, context_data)
                    else:
                        context_data["data"] = result['Error']
                        context_data["is_error"] = True
                        return render(request, self.template_name, context_data)
                return render(request, self.template_name, context_data)

            except Exception as e:
                context_data["data"] = e
                context_data["is_error"] = True
        return render(request, self.template_name, {"form": form})


# class TestHomeTemplateView(TemplateView):
#     template_name = "auth_app/home/test_home.html"


# class ProfileTemplateView(TemplateView):
#     template_name = "auth_app/profile/auth-profile.html"


# class DashboardHomeView(TemplateView):
#     template_name = "partials/main/main.html"
