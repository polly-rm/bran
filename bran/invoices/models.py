from decimal import Decimal

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
    invoice_name = models.CharField(
        max_length=150
    )
    invoice_address = models.CharField(
        max_length=150
    )
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
    time_to_collect = models.DateTimeField(
        blank=True,
        null=True
    )
    time_to_deliver = models.DateTimeField(
        blank=True,
        null=True,
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    pdf_file = models.FileField(
        upload_to='invoices/',
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    additional_service_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    additional_service_description = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    additional_service_quantity = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    additional_service_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    @property
    def unit_total(self):
        return self.quantity * self.unit_cost

    @property
    def additional_service_total(self):
        total = 0

        if self.additional_service_quantity and self.additional_service_cost:
            total += self.additional_service_cost * self.additional_service_quantity
        elif self.additional_service_cost:
            total += self.additional_service_cost

        return total

    @property
    def subtotal(self):
        return self.unit_total + self.additional_service_total

    @property
    def vat(self):
        return self.subtotal * Decimal('0.20')  # 20% VAT

    @property
    def total(self):
        return self.subtotal + self.vat

    def __str__(self):
        return f'Invoice #{self.invoice_number}'

    def save(self, *args, **kwargs):
        if self.invoice_number is None:
            last_number = Invoice.objects.aggregate(Max('invoice_number'))['invoice_number__max']
            self.invoice_number = 1 if last_number is None else last_number + 1
        super().save(*args, **kwargs)
