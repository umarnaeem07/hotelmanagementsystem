from django.urls import path

from .views import StaffInvitationAPIView

urlpatterns = [
    path(
        "staff/invitations/",
        StaffInvitationAPIView.as_view(),
        name="staff-invitations"
    ),
]