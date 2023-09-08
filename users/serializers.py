# users/serlizers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress
from translations.models import Language


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
    confirm_password = serializers.CharField(required=True, write_only=True)
    language = serializers.CharField(required=True, write_only=True)
    accepted_terms = serializers.BooleanField(required=True, write_only=True)
    accepted_privacy = serializers.BooleanField(required=True, write_only=True)
    accepted_marketing = serializers.BooleanField(required=True, write_only=True)


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
        
        if not data['accepted_terms']:
            raise serializers.ValidationError(
                {'accepted_terms': _('You must accept terms and conditions')})
        
        if not data['accepted_privacy']:
            raise serializers.ValidationError(
                {'accepted_privacy': _('You must accept privacy policy')})
        
        # find language code
        try:
            language = Language.objects.get(code=data['language'])
        except Language.DoesNotExist:
            data['language'] = 'es'

        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.profile.language = Language.objects.get(code=validated_data['language'])
        user.profile.accepted_terms = validated_data['accepted_terms']
        user.profile.accepted_privacy = validated_data['accepted_privacy']
        user.profile.accepted_marketing = validated_data['accepted_marketing']

        user.save()

        return user
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password','language', 'accepted_terms', 'accepted_privacy', 'accepted_marketing')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('confirm_password', 'language', 'accepted_terms', 'accepted_privacy', 'accepted_marketing', 'avatar',)

