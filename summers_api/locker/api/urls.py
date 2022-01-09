from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# from summers_api.locker.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "summers_api.locker"

urlpatterns = router.urls
