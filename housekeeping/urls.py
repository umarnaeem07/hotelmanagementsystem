from django.urls import path

from .views import (
    HousekeepingTaskListCreateAPIView,
    HousekeepingTaskDetailAPIView,
)

urlpatterns = [
    path(
        "housekeeping/",
        HousekeepingTaskListCreateAPIView.as_view(),
        name="housekeeping-list-create"
    ),

    path(
        "housekeeping/<int:pk>/",
        HousekeepingTaskDetailAPIView.as_view(),
        name="housekeeping-detail"
    ),
]