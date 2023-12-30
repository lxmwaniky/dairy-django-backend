from django.db.models.signals import pre_save
from django.dispatch import receiver

from production.models import Milk


@receiver(pre_save, sender=Milk)
def set_lactation_for_new_milk(sender, instance, **kwargs):
    if instance.lactation is None:
        # Fetch the most recent lactation for the cow
        most_recent_lactation = instance.cow.lactations.latest()

        if most_recent_lactation:
            instance.lactation = most_recent_lactation
