from django.conf import settings
from rest_framework_nested.routers import (
    DefaultRouter,
    NestedDefaultRouter,
    NestedSimpleRouter,
    SimpleRouter,
)

from summers_api.locker.api import views

if settings.DEBUG:
    router = DefaultRouter()
    nested_router = NestedDefaultRouter
else:
    router = SimpleRouter()
    nested_router = NestedSimpleRouter

app_name = "summers_api.locker"

router.register("categories", views.CategoryViewSet)
router.register("vaults", views.VaultViewSet)


vaults_router = nested_router(router, r"vaults", lookup="vault")
vaults_router.register(r"folders", views.FolderViewSet, basename="vault-folders")


folders_router = nested_router(vaults_router, r"folders", lookup="folder")
folders_router.register(r"notes", views.NoteViewSet, basename="folder-notes")


urlpatterns = router.urls + vaults_router.urls + folders_router.urls
