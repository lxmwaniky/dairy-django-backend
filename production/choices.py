from django.db import models


class LactationStageChoices(models.TextChoices):
    """
    Choices for the stage of lactation.

    Choices:
    - `EARLY`: Early stage of lactation.
    - `MID`: Mid stage of lactation.
    - `LATE`: Late stage of lactation.
    - `DRY`: Dry stage (post-lactation).
    - `ENDED`: Lactation has ended.

    Usage:
        These choices represent the stage of lactation in the Lactation model and are utilized in the LactationManager
        to determine lactation stages based on the number of days.

    Example:
        ```
        class Lactation(models.Model):
            lactation_stage = models.CharField(
                max_length=5,
                choices=LactationStageChoices.choices,
                default=LactationStageChoices.DRY,
            )
        ```

    Manager Usage:
        The `LactationManager` uses these choices in the `lactation_stage` method to determine the stage of lactation
        based on the number of days.

    Example:
        ```
        class LactationManager(models.Manager):
            ...

            def lactation_stage(self, lactation):
                days_in_lactation = self.days_in_lactation(lactation)

                if lactation.end_date:
                    return LactationStageChoices.ENDED
                elif days_in_lactation <= 100:
                    return LactationStageChoices.EARLY
                elif days_in_lactation <= 200:
                    return LactationStageChoices.MID
                elif days_in_lactation <= 275:
                    return LactationStageChoices.LATE
                else:
                    return LactationStageChoices.DRY
        ```
    """

    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"
    DRY = "Dry"
    ENDED = "Ended"
