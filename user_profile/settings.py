from django.conf import settings

USERPROFILE_SETTINGS = {
    'app_verbose_name': "Custom User",
    'register_proxy_auth_group_model': True,
}

if hasattr(settings, 'USERPROFILE'):
    USERPROFILE_SETTINGS.update(settings.USERPROFILE)
