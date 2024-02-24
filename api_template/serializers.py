from rest_framework import serializers
from .models import UserAccounts

class UserAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccounts
        # fields = ["IdNumber", "FullName", "Username", "Password", "Section", "Role"]
        fields = '__all__'