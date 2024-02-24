from django.contrib import admin
from .models import UserAccounts

# Register your models here.

class UserAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'IdNumber', 'FullName', 'Username', 'Section', 'Role')

admin.site.register(UserAccounts, UserAccountsAdmin)