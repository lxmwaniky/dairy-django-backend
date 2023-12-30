from django.db.models.signals import pre_save
from django.dispatch import receiver

from production.models import Milk


@receiver(pre_save, sender=Milk)
def set_lactation_for_new_milk(sender, instance, **kwargs):
    """
    Signal handler for setting the associated lactation for a new milk record.

    This signal is triggered before saving a Milk instance. If the lactation field
    of the milk record is not explicitly set, it automatically fetches the most recent
    lactation associated with the cow and assigns it to the milk record.

    Args:
    - `sender`: The sender of the signal (Milk model in this case).
    - `instance`: The Milk instance being saved.
    - `kwargs`: Additional keyword arguments passed to the signal handler.

    Usage:
        This signal ensures that every new milk record is associated with the correct lactation.
        It checks if the lactation field is None and, if so, fetches the most recent lactation
        for the corresponding cow and assigns it to the milk record.
    """
    if instance.lactation is None:
        # Fetch the most recent lactation for the cow
        most_recent_lactation = instance.cow.lactations.latest()

        if most_recent_lactation:
            instance.lactation = most_recent_lactation
