# users/serlizers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    profile = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'email', 'profile',)
        read_only_fields = ('id', 'email', 'profile',)


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('user', 'address_type', 'address', 'city',
                  'province', 'zip_code', 'created_at', 'updated_at', 'nie', 'get_avatar')
        read_only_fields = ('user', 'address_type', 'address', 'city',
                            'province', 'zip_code', 'created_at', 'updated_at', 'nie')

    def get_avatar(self, obj):
        if obj.user.profile.avatar:
            return obj.user.profile.avatar.url
        else:
            return None


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            raise serializers.ValidationError(
                {'email': _('Email already exists')})
        except User.DoesNotExist:
            pass

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'password': _('Passwords must match')})

        return data

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password',
                  'first_name', 'last_name', 'phone', 'nie')
        extra_kwargs = {'password': {'write_only': True}}
