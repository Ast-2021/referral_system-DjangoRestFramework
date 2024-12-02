from rest_framework import serializers
from .models import CustomUser


class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'invite_code', 'is_active'] 


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number']
            )
        return user
