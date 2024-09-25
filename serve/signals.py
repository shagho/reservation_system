from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ReservationRequest
from .tasks import send_inform



@receiver(pre_save, sender=ReservationRequest)
def pre_save_reservation_handler(sender, instance, **kwargs):
    if instance.pk:
        if instance.status in ['accepted', 'not accept']:
            send_inform.delay(instance.user.username, instance.get_status_display())
