from django.urls import path

from .views import AcceptInvitationAPIView, StaffInvitationAPIView

urlpatterns = [
    path(
        "staff/invitations/",
        StaffInvitationAPIView.as_view(),
        name="staff-invitations"
    ),
    path(
        "staff/accept-invitation/<uuid:token>/",
        AcceptInvitationAPIView.as_view(),
        name="accept-invitation",
    ),
]