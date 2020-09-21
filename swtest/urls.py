from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import djoser_urls

admin.site.site_header = "Адмнистрирование swtest"
admin.site.site_title = "Адмнистрирование swtest"
admin.site.index_title = "swtest"

ver_tag = 'v1'
prefix = f'api/{ver_tag}/'

schema_view = get_schema_view(
    openapi.Info(
        title="Nav Info API",
        default_version=ver_tag,
        contact=openapi.Contact(
            name="Nikolay Bely",
            url="https://github.com/alldevic",
            email="stdfo@ya.ru"),
        license=openapi.License(
            name="MIT License",
            url="https://github.com/alldevic/swtest/blob/master/LICENSE"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(prefix, schema_view.with_ui('swagger',
                                     cache_timeout=0), name='docs-ui'),
    re_path(rf'^{prefix}swtest_openapi(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{prefix}auth/', include('djoser.urls.authtoken')),
    path(f'{prefix}', include(djoser_urls)),
    path(f'{prefix}', include('friends.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # Silk profiler
    urlpatterns = [
        path('silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns
