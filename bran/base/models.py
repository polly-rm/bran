from django.db import models


class TimeStampedModel(models.Model):
    """An abstract model class which provides `created` and `updated`
    fields.
    """
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class SendEmail(TimeStampedModel):
    email_from = models.EmailField()
    email_to = models.EmailField()
    subject = models.CharField(
        max_length=256
    )
    message = models.TextField()
    is_sent = models.BooleanField()
