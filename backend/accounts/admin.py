"""
Accounts Admin Configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

# Customize the default User admin if needed
# admin.site.unregister(User)
# admin.site.register(User, BaseUserAdmin)
