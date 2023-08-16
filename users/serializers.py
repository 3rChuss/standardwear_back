# users/serlizers.py
from rest_framework import serializers
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
