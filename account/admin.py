from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# 创建内联
class ProfileInline(admin.StackedInline):

    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"

# Define a new User admin
# 把用户身份profile添加到用户user页内
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline,]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
