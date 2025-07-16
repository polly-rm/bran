from django.db import models
from django.db.models import Max

from bran.base.models import TimeStampedModel
from bran.quotes.models import Quote


class Invoice(TimeStampedModel):
    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name='invoices',
        blank=True,
        null=True
    )
    invoice_number = models.PositiveIntegerField(
        unique=True
    )
    name = models.CharField(
        max_length=50
    )
    invoice_name = models.CharField(
        max_length=150
    )
    invoice_address = models.CharField(
        max_length=150
    )
    contact_telephone = models.CharField(
        max_length=50
    )
    email = models.EmailField()
    postcode_from = models.CharField(
        max_length=150
    )
    postcode_to = models.CharField(
        max_length=150
    )
    company_from = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    company_to = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    time_to_collect_from = models.CharField(
        max_length=100
    )
    time_to_collect_to = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    time_to_deliver_from = models.CharField(
        max_length=100
    )
    time_to_deliver_to = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    additional_info = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Invoice #{self.invoice_number}'

    def save(self, *args, **kwargs):
        if self.invoice_number is None:
            last_number = Invoice.objects.aggregate(Max('invoice_number'))['invoice_number__max']
            self.invoice_number = 1 if last_number is None else last_number + 1
        super().save(*args, **kwargs)
