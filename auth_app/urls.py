from django.urls import path
from .views import (
    RequestPhoneView,
    VerifyRequestPhoneView,
    logout_view,
    ProfileView,
    CivilRegistryView,
    LogOutTemplateView,
    TestHomeTemplateView,
)

app_name = "auth_app"

urlpatterns = [
    path("request_phone/", RequestPhoneView.as_view(), name="login"),
    path("verify_phone/", VerifyRequestPhoneView.as_view(), name="verify"),
    path("logout_user/", logout_view, name="logout"),
    path("profile_detail/", ProfileView.as_view(), name="profile_detail"),
    path("civil_registry/", CivilRegistryView.as_view(), name="civil_registry"),
    path("logout_template/", LogOutTemplateView.as_view(), name="logout_template"),
    path("test_home/", TestHomeTemplateView.as_view(), name="test_home"),
]
