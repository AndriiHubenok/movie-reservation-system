from rest_framework import serializers

from movies.models import Showtime, Seat
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'seat', 'status', 'created_at']

        read_only_fields = ['status']

    def validate(self, attrs):
        showtime = attrs.get('showtime')
        seat = attrs.get('seat')

        if showtime.hall != seat.hall:
            raise serializers.ValidationError("The selected seat does not belong to the hall of the selected showtime.")

        if Reservation.objects.filter(showtime=showtime, seat=seat).exists():
            raise serializers.ValidationError("This seat is already reserved for the selected showtime.")

        return attrs