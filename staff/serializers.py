from rest_framework import serializers
from accounts.models import User
from .models import StaffInvitation


class StaffInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffInvitation
        fields = (
            "id",
            "email",
            "role",
            "accepted",
            "created_at",
        )
        read_only_fields = (
            "accepted",
            "created_at",
        )

    def validate_email(self, value):

        request = self.context["request"]
        hotel = request.user.hotel

        exists = StaffInvitation.objects.filter(
            hotel=hotel,
            email=value,
            accepted=False
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "A pending invitation already exists for this email."
            )

        return value
class AcceptInvitationSerializer(
    serializers.Serializer
):

    username = serializers.CharField(
        max_length=150
    )

    password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if (
            attrs["password"] !=
            attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                "Passwords do not match."
            )

        if User.objects.filter(
            username=attrs["username"]
        ).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return attrs