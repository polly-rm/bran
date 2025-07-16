from django.contrib import admin

from bran.invoices.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number',
                    'created',
                    'invoice_name',
                    'invoice_address']
    search_fields = ['invoice_number',
                     'created',
                     'invoice_name',
                     'invoice_address']

    def get_changeform_initial_data(self, request):
        return request.GET.dict()
