from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as StockGroup
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import UserProfile, Group
from .settings import USERPROFILE_SETTINGS


@admin.register(UserProfile)
class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/user_profile/user_profile/add_form.html'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'nickname', 'description')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'nickname', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'nickname')
    ordering = ('email',)


if USERPROFILE_SETTINGS['register_proxy_auth_group_model']:
    admin.site.unregister(StockGroup)

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin):
        pass
