from django.db import models

from bran.base.models import TimeStampedModel


class Quote(TimeStampedModel):
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
    time_to_collect_from = models.DateTimeField()
    time_to_collect_to = models.DateTimeField(
        blank=True,
        null=True
    )
    time_to_deliver_from = models.DateTimeField()
    time_to_deliver_to = models.DateTimeField(
        blank=True,
        null=True
    )
    additional_info = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Quote #{self.id} from {self.email}"


class Parcel(TimeStampedModel):
    quote = models.ForeignKey(
        Quote,
        related_name='parcels',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Parcel #{self.id} for Quote #{self.quote.id} from {self.quote.name}"
