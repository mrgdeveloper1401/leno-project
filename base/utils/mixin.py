from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class RedirectAuthenticatedUserMixin(AccessMixin):
    redirect_authenticated_to = "auth_app:test_home"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = self.get_redirect_authenticated_url()
            if redirect_to:
                return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_authenticated_url(self):
        return self.redirect_authenticated_to
