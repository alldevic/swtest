from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("users/me", views.MeViewSet, basename="usersme")

urlpatterns = router.urls
