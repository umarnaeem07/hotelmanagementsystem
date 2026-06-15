from rest_framework.permissions import BasePermission
from .models import Staff


class IsHotelStaff(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return Staff.objects.filter(
            user=request.user
        ).exists()


class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(
        self,
        request,
        view
    ):

        try:
            staff = Staff.objects.get(
                user=request.user
            )
        except Staff.DoesNotExist:
            return False

        return (
            staff.role in
            self.allowed_roles
        )


class IsOwner(HasRole):

    allowed_roles = [
        "owner"
    ]


class IsManagerOrOwner(
    HasRole
):

    allowed_roles = [
        "owner",
        "manager"
    ]


class IsReceptionistOrAbove(
    HasRole
):

    allowed_roles = [
        "owner",
        "manager",
        "receptionist"
    ]


class IsHousekeepingOrOwner(
    HasRole
):

    allowed_roles = [
        "owner",
        "housekeeping"
    ]


class IsCashierOrOwner(
    HasRole
):

    allowed_roles = [
        "owner",
        "cashier"
    ]