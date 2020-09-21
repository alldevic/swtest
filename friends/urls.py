from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("users/me", views.MeViewSet, basename="usersme")
router.register("users", views.UserIdViewSet, basename="usersid")

urlpatterns = router.urls
