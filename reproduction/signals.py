from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Cow
from production.models import Lactation
from reproduction.choices import PregnancyOutcomeChoices
from reproduction.models import Pregnancy


@receiver(post_save, sender=Pregnancy)
def create_lactation(sender, instance, **kwargs):
    if not instance.date_of_calving and instance.pregnancy_outcome not in [
        PregnancyOutcomeChoices.LIVE,
        PregnancyOutcomeChoices.STILLBORN,
    ]:
        return

    Cow.objects.mark_a_recently_calved_cow(instance.cow)

    try:
        previous_lactation = Lactation.objects.filter(cow=instance.cow).latest()

        if previous_lactation and not previous_lactation.end_date:
            previous_lactation.end_date = instance.date_of_calving - timedelta(days=1)
            previous_lactation.save()

            Lactation.objects.create(
                start_date=instance.date_of_calving,
                cow=instance.cow,
                pregnancy=instance,
                lactation_number=previous_lactation.lactation_number + 1,
            )
    except Lactation.DoesNotExist:
        Lactation.objects.create(
            start_date=instance.date_of_calving, cow=instance.cow, pregnancy=instance
        )
