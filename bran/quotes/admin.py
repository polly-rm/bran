from urllib.parse import urlencode

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.dateformat import format

from bran.invoices.models import Invoice
from bran.quotes.models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'created',
                    'email',
                    'name',
                    'postcode_from',
                    'postcode_to',
                    'my_button_field']
    search_fields = ['email',
                     'name',
                     'postcode_from',
                     'postcode_to',
                     'company_from',
                     'company_to',
                     'invoice_name',
                     'invoice_address']

    def my_button_field(self, obj):
        url = reverse('admin:create-invoice', args=[obj.id])
        return format_html(
            '<a class="button" style="padding: 5px 10px; background-color: #5e9ed6; color: white; text-decoration: none; border-radius: 4px;" href="{}">Create Invoice</a>',
            url
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-invoice/<int:quote_id>/', self.admin_site.admin_view(self.create_invoice_view),
                 name='create-invoice'),
        ]
        return custom_urls + urls

    def create_invoice_view(self, request, quote_id):
        quote = Quote.objects.get(pk=quote_id)

        # Optional: get the next invoice number but don't save it
        last_invoice = Invoice.objects.order_by('-invoice_number').first()
        next_number = (last_invoice.invoice_number + 1) if last_invoice else 1

        # Build initial data as GET query params
        data = {
            'quote': quote_id,
            'invoice_number': next_number,
            'invoice_name': quote.invoice_name,
            'invoice_address': quote.invoice_address,
            'postcode_from': quote.postcode_from,
            'postcode_to': quote.postcode_to,
            'company_from': quote.company_from,
            'company_to': quote.company_to,
            'time_to_collect': format(quote.time_to_collect_from, 'Y-m-d H:i:s'),
            'time_to_deliver': format(quote.time_to_deliver_from, 'Y-m-d H:i:s'),
            'quantity': sum(list(quote.parcels.values_list('count', flat=True))),
        }

        # Redirect to the add invoice form with prefilled data
        query_string = urlencode({k: v for k, v in data.items() if v is not None})
        return HttpResponseRedirect(f"/admin/invoices/invoice/add/?{query_string}")
