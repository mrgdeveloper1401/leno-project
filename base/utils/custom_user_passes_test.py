from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View

class CustomLoginRequiredMixin(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect('auth_app:home')
        return super().dispatch(request, *args, **kwargs)
