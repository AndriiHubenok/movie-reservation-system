from rest_framework import serializers

from movies.models import Showtime, Seat
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'seat', 'status', 'created_at']

        read_only_fields = ['status']