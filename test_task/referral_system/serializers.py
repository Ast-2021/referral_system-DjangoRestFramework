from rest_framework import serializers
from .models import CustomUser


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'invite_code', 'my_refer']

class UserSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'invite_code', 'my_refer', 'referrals']

    def get_referrals(self, obj):
        referrals = CustomUser.objects.filter(my_refer=obj.invite_code)
        return ReferralSerializer(referrals, many=True).data
    
    def to_representation(self, instance): 
        ret = super().to_representation(instance) 
        if not ret['my_refer']: 
            ret.pop('my_refer') 
        return ret


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CustomUser
        fields = ['my_refer']


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
