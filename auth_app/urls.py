from django.urls import path
from .views import (
    RequestPhoneView,
    VerifyRequestPhoneView,
    logout_view,
    ProfileView
)

app_name = "auth_app"

urlpatterns = [
    path("request_phone/", RequestPhoneView.as_view(), name="login"),
    path("verify_phone/", VerifyRequestPhoneView.as_view(), name="verify"),
    path("logout_user/", logout_view, name="logout"),
    path("profile_detail/", ProfileView.as_view(), name="profile_detail"),
]
