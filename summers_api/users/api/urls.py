from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from summers_api.users.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "summers_api.users"

router.register("auth", views.AuthViewSet)

urlpatterns = router.urls
