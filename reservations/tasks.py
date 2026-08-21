from celery import shared_task
from .models import Reservation

@shared_task
def cancel_unpaid_reservation(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        if reservation.status == 'pending':
            reservation.status = 'cancelled'
            reservation.save()
            return f"Reservation {reservation_id} cancelled due to timeout."
        return f"Reservation {reservation_id} is already confirmed."

    except Reservation.DoesNotExist:
        return f"Reservation {reservation_id} not found."