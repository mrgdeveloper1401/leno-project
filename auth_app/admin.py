# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from .models import User
#
#
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {"fields": ("phone", "password")}),
#         (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     # "groups",
#                     # "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("phone", "usable_password", "password1", "password2"),
#             },
#         ),
#     )
#     list_display = ("phone", "email", "first_name", "last_name", "is_staff", "is_active", "is_superuser", "created_at")
#     list_filter = ("is_staff", "is_superuser", "is_active")
#     search_fields = ("phone",)
#     ordering = ("-id",)
#     filter_horizontal = []
#     readonly_fields = ("created_at", "updated_at")
