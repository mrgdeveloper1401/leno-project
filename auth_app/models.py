from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from .managers import CoustomUserManager


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, CreateMixin, UpdateMixin):
    # TODO, add field verify
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ("email",)

    objects = CoustomUserManager()

    class Meta:
        ordering = ("-id",)
        db_table = "auth_user"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

    def _user_has_module_perms(self, user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_module_perms"):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return self._user_has_module_perms(self, app_label)