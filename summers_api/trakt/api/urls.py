from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "summers_api.trakt"

router.register("shows", views.ShowModelViewSet)
urlpatterns = router.urls
