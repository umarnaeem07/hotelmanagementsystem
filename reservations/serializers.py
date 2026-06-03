from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"

        read_only_fields = (
            "hotel",
            "total_amount",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):

        request = self.context["request"]

        hotel = request.user.hotel

        guest = attrs.get("guest")
        room = attrs.get("room")

        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")

        # Check dates
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        # Guest must belong to current user's hotel
        if guest.hotel != hotel:
            raise serializers.ValidationError(
                "Selected guest does not belong to your hotel."
            )

        # Room must belong to current user's hotel
        if room.hotel != hotel:
            raise serializers.ValidationError(
                "Selected room does not belong to your hotel."
            )

        # Prevent double booking
        reservations = Reservation.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exclude(
            status="cancelled"
        )

        # Ignore current reservation during update
        if self.instance:
            reservations = reservations.exclude(
                pk=self.instance.pk
            )

        if reservations.exists():
            raise serializers.ValidationError(
                "Room is already booked for these dates."
            )

        return attrs