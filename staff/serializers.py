from rest_framework import serializers

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