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

    def __str__(self):
        return f'Message from {self.email_from}'

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
