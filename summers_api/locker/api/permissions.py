from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from summers_api.locker.models import Folder, Vault


class VaultOwnPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if user own Vault for Vault get, update, delete or any operations
        on vault endpoints.
        """
        if request.user and request.user.is_authenticated:
            """vault_pk comes for nested routes and pk comes from only vault's route.

            ie.
            - Vault route
            GET `/vaults/pk/`

            - Vault's nested routes
            GET `/vaults/vault_pk/folders/`

            Thats why first checking if there is vault_pk take it otherwise pk for vault routes.
            """
            vault = get_object_or_404(
                Vault,
                pk=(
                    view.kwargs.get("vault_pk")
                    or request.GET.get("vault_id")
                    or view.kwargs["pk"]
                ),
            )

            if vault.user == request.user:
                return True

        return False


class VaultAndFolderOwnPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if user own Vault and folder for folder get, create, update, delete or any
        other operations on folder level routes.
        """
        if request.user and request.user.is_authenticated:
            """vault_pk comes for nested routes and pk comes from only vault's route.

            - Vault route
            GET `/vaults/pk/`

            - Vault's nested routes
            GET `/vaults/vault_pk/folders/`

            Thats why first checking if there is vault_pk take it otherwise pk for vault routes.

            -----------------------------------------------------------------------------------
            folder_pk comes for nested routes and pk comes from only folder's route.

            - Folder route
            GET `/vaults/vault_pk/folders/pk/`

            - Folder's nested routes
            GET `/vaults/vault_pk/folders/folder_pk/notes/`

            Thats why first checking if there is folder_pk take it otherwise pk for folder routes.
            """
            vault = get_object_or_404(
                Vault, pk=(view.kwargs.get("vault_pk") or view.kwargs["pk"])
            )

            folder = get_object_or_404(
                Folder, pk=(view.kwargs.get("folder_pk") or view.kwargs["pk"])
            )

            if vault.user == request.user and folder.vault.user == request.user:
                return True

        return False
