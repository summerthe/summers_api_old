from django.conf import settings
from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = [
    path("", include("summers_api.users.api.urls")),
    path("trakt/", include("summers_api.trakt.api.urls")),
    path("locker/", include("summers_api.locker.api.urls")),
]
urlpatterns += router.urls
