from django.urls import path

from .views import (
    HotelSettingAPIView
)

urlpatterns = [

    path(
        "settings/",
        HotelSettingAPIView.as_view(),
        name="settings"
    ),

]