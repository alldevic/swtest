from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

from . import djoser_views

router = DefaultRouter()
router.register("users", djoser_views.UserViewSet)

User = get_user_model()

urlpatterns = router.urls
