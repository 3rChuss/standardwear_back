# users/admin.py
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, User, UserAddress, UserMembership
from .forms import CustomUserCreationForm, CustomUserChangeForm
from . import constants as user_constants


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_plural_name = "User Profile"
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = ['email']
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline,)
    list_display = ('get_avatar', 'email', 'is_staff', 'is_active', 'is_superuser',
                    'user_type', 'get_nie', 'first_name', 'last_name', 'get_phone', )
    list_filter = ('email', 'is_staff', 'is_active',
                   'is_superuser', 'user_type')
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'user_type',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'user_type')}
         ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_nie(self, obj):
        return obj.profile.nie
    get_nie.short_description = _('NIE')

    def get_phone(self, obj):
        return obj.profile.phone
    get_phone.short_description = 'Phone'

    def get_avatar(self, obj):
        # image with link to edit

        return format_html(
            '<a href="{}"><img src="{}" width="50" height="50" /></a>',
            '/admin/users/user/{}/change/'.format(obj.id),
            obj.profile.avatar.url if obj.profile.avatar else '/staticfiles/img/default_avatar.png',
        )

    get_avatar.short_description = 'Avatar'


class CustomUserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'address', 'city', 'province',)
    list_filter = ('user', 'address_type', 'city', 'province',)
    search_fields = ('user', 'address_type', 'address', 'city', 'province',)


class CustomMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'membership_start',
                    'membership_end', 'get_membership_status',)
    list_filter = ('user', 'membership_type', 'membership_start',
                   'membership_end', )
    search_fields = ('user', 'membership_type', 'membership_start',
                     'membership_end', 'get_membership_status',)

    def get_membership_status(self, obj):
        if obj.membership_type == user_constants.MEMBERSHIP_FREE:
            return format_html(
                '<span style="color: #{};">{}</span>',
                'FF0000',
                'Free'
            )
        if obj.membership_end < timezone.now():
            return format_html(
                '<span style="color: #{};">{}</span>',
                'FF0000',
                'Expired'
            )
        else:
            return format_html(
                '<span style="color: #{};">{}</span>',
                '008000',
                'Active'
            )

    get_membership_status.short_description = 'Status'


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAddress, CustomUserAddressAdmin)
admin.site.register(UserMembership, CustomMembershipAdmin)
