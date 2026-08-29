from rest_framework.permissions import BasePermission
from .models import Staff


class IsHotelStaff(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if Staff.objects.filter(
            user=request.user
        ).exists():
            return True

        hotel = getattr(request.user, "hotel", None)
        return bool(hotel and hotel.owner_id == request.user.id)


class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(
        self,
        request,
        view
    ):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        try:
            staff = Staff.objects.get(
                user=request.user
            )
        except Staff.DoesNotExist:
            hotel = getattr(request.user, "hotel", None)
            if hotel and hotel.owner_id == request.user.id:
                return "owner" in self.allowed_roles
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